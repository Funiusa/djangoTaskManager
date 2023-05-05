from multiprocessing.pool import AsyncResult
from typing import Any

from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from task_manager import settings, tasks
from .models import User, Task, Tag, Developer
from django.core.files.base import File


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone",
            "password",
            "email",
            "role",
            "avatar_picture",
        )


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ("id", "username", "email")


class DeveloperRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username

    def to_internal_value(self, data):
        try:
            return Developer.objects.get(username=data)
        except Developer.DoesNotExist:
            raise serializers.ValidationError("Developer does not exist")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
        )
        read_only_fields = ("id", "u_id")


class TagRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title

    def to_internal_value(self, data):
        try:
            return Tag.objects.get(title=data)
        except Tag.DoesNotExist:
            raise serializers.ValidationError("Tag does not exist")


class TaskSerializer(serializers.ModelSerializer):
    assigned_by = serializers.CharField(source="assigned_by.username", read_only=True)
    assigned_to = DeveloperRelatedField(queryset=Developer.objects.all(), many=True)
    tags = TagRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "assigned_by",
            "assigned_to",
            "tags",
            "description",
            "deadline_date",
            "state",
            "priority",
        )


class RepresentationSerializer(serializers.Serializer):
    def update(self, instance: Any, validated_data: dict) -> Any:
        pass

    def create(self, validated_data: dict) -> Any:
        pass


class CountdownJobSerializer(RepresentationSerializer):
    seconds = serializers.IntegerField(write_only=True)

    task_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data: dict) -> AsyncResult:
        return tasks.countdown.delay(**validated_data)


class ErrorSerializer(RepresentationSerializer):
    non_field_errors: serializers.ListSerializer = serializers.ListSerializer(
        child=serializers.CharField()
    )


class JobSerializer(RepresentationSerializer):
    task_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    errors = ErrorSerializer(read_only=True, required=False)
    result = serializers.CharField(required=False)
