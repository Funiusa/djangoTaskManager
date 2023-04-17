from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices, db_index=True
    )
    password = models.CharField(max_length=128, blank=True)
    REQUIRED_FIELDS = ["role", "email"]

    def __str__(self):
        return f"{self.username}"

    class Meta:
        ordering = ["username", "id"]


class Admin(User):
    base_role = User.Roles.ADMIN
    is_superuser = True
    is_staff = True

    class Meta:
        proxy = True


class Manager(User):
    base_role = User.Roles.MANAGER

    class Meta:
        proxy = True


class Developer(User):
    base_role = User.Roles.DEVELOPER

    class Meta:
        proxy = True
