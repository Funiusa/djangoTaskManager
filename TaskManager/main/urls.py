from .admin import task_manager_admin_site
from django.urls import path

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
]
