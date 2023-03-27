from rest_framework import serializers
from .models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "last_name",
            "role",
            "is_staff",
            "is_active",
            "email",
        )

    def create(self, validated_data):
        return User(**validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "u_id", "title")
        read_only_fields = ("id", "u_id")

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
    assigned_by = serializers.CharField(source="assigned_by.username", read_only=True)
    tags = TagSerializer
    assigned_to = UserSerializer

    @staticmethod
    def get_assigned_to(obj):
        return [user.username for user in obj.assigned_to.all()]

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "deadline_date",
            "creation_date",
            "assigned_by",
            "assigned_to",
            "tags",
            "state",
            "priority",
        )
