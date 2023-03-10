from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices, db_index=True
    )

    REQUIRED_FIELDS = ["role", "email"]

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        ordering = ["username", "id"]


class Admin(User):
    base_role = User.Roles.ADMIN
    is_superuser = True
    is_staff = True

    def __str__(self):
        return self.base_role

    class Meta:
        proxy = True


class Manager(User):
    base_role = User.Roles.MANAGER

    def __str__(self):
        return self.base_role

    class Meta:
        proxy = True


class Developer(User):
    base_role = User.Roles.DEVELOPER

    def __str__(self):
        return self.base_role

    class Meta:
        proxy = True
