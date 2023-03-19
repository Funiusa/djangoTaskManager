from rest_framework import serializers
from .models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "role",
            "is_staff",
            "is_active",
            "email",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "u_id", "title")


class TaskSerializer(serializers.ModelSerializer):
    assigned_by = serializers.StringRelatedField(source="assigned_by.username")
    assigned_to = serializers.SerializerMethodField()
    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    @staticmethod
    def get_assigned_to(obj):
        return [user.username for user in obj.assigned_to.all()]

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "creation_date",
            "assigned_by",
            "assigned_to",
            "tags",
            "state",
            "priority",
        )
