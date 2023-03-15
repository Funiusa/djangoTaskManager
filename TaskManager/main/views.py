from rest_framework import viewsets
from .models import User, Task, Tag
from .serializer import UserSerializer, TagSerializer, TaskSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related()
    serializer_class = TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
