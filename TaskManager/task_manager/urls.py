"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main.services.single_resource import BulkRouter
from main import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Dualboot learn django API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = BulkRouter()
users = router.register(
    r"users",
    views.UserViewSet,
    basename="users",
)
users.register(
    r"tasks",
    views.UserTasksViewSet,
    basename="user_tasks",
    parents_query_lookups=["assigned_by_id"],
)
tasks = router.register(r"tasks", views.TaskViewSet, basename="tasks")
tasks.register(
    r"tags",
    views.TaskTagsViewSet,
    basename="task_tags",
    parents_query_lookups=["task_id"],
)
router.register(
    r"tasks",
    views.TaskViewSet,
    basename="tasks",
)
router.register(
    r"tags",
    views.TagViewSet,
    basename="tags",
)
router.register(r"current-user", views.CurrentUserViewSet, basename="current_user")
router.register(r"countdown", views.CountdownJobViewSet, basename="countdown")
router.register(r"jobs", views.AsyncJobViewSet, basename="jobs")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
