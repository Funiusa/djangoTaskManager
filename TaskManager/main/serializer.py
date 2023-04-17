from rest_framework import serializers
from .models import User, Task, Tag, Developer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "last_name",
            "email",
            "role",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.role = validated_data.get("role", instance.role)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance


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
