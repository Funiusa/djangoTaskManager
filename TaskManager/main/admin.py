from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Task, Tag


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAmin(admin.ModelAdmin):
    pass


class UserAdmin(BaseUserAdmin):
    list_display = ["id", "username", "email", "role", "is_active", "is_staff"]
    add_fieldsets = (
        (
            "Required information",
            {
                "fields": (
                    "username",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Additional fields",
            {
                "fields": (
                    "date_of_birth",
                    "phone",
                )
            },
        ),
    )


task_manager_admin_site.register(User, UserAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Task)
admin.site.register(Tag)
