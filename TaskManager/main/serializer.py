from rest_framework import serializers
from .models import User, Task, Tag, Developer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "password",
            "date_of_birth",
            "phone",
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
