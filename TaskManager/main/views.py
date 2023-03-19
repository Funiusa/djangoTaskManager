
import django_filters
from rest_framework import viewsets
from .models import User, Task, Tag
from .serializer import UserSerializer, TagSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend]


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(field_name="state", lookup_expr="icontains")
    assigned_by = django_filters.CharFilter(
        field_name="assigned_by__username",
        lookup_expr="icontains",
    )
    assigned_to = django_filters.CharFilter(
        field_name="assigned_to__username",
        lookup_expr="icontains",
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__title", to_field_name="title", queryset=Tag.objects.all()
    )

    class Meta:
        model = Task
        fields = ("state", "tags", "assigned_by", "assigned_to")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related().order_by("id")
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
