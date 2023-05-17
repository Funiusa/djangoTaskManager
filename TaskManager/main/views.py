from typing import cast, Any

import django_filters
from django.http import Http404, HttpResponse
from rest_framework import viewsets, status, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from main.services.async_celery import AsyncJob, JobStatus
from .models import User, Task, Tag
from .permission import IsStaffPermission
from .serializer import (
    UserSerializer,
    TagSerializer,
    TaskSerializer,
    CountdownJobSerializer,
    JobSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend

from .services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="username", lookup_expr="icontains"
    )

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        pk = self.kwargs.get("pk")

        if pk == "current":
            return self.request.user

        return super().get_object()


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
    tags = django_filters.CharFilter(
        field_name="tags__title",
        lookup_expr="icontains",
    )

    class Meta:
        model = Task
        fields = ("state", "tags", "assigned_by", "assigned_to")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related().order_by("id")
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsStaffPermission)

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, IsStaffPermission)


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("assigned_by")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer


class TaskTagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class CountdownJobViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CountdownJobSerializer

    def get_success_headers(self, data: dict) -> dict[str, str]:
        task_id = data["task_id"]
        return {"Location": reverse("jobs-detail", args=[task_id])}


class AsyncJobViewSet(viewsets.GenericViewSet):
    serializer_class = JobSerializer

    def get_object(self) -> AsyncJob:
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        task_id = self.kwargs[lookup_url_kwargs]
        job = AsyncJob.from_id(task_id)
        if job.status == JobStatus.UNKNOWN:
            raise Http404()
        return job

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data
        if instance.status == JobStatus.SUCCESS:
            location = self.request.build_absolute_uri(instance.result)
            return Response(
                serializer_data,
                headers={"location": location},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer_data)
