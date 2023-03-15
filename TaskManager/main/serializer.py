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
            "email",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("u_id", "title")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        users = UserSerializer(required=True)
        tags = TagSerializer(required=False)
        fields = (
            "id",
            "title",
            "description",
            "creation_date",
            "users",
            "tags",
            "state",
            "priority",
        )
