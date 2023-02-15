from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices
    )


class Admin(User):
    base_role = User.Roles.ADMIN
    is_superuser = True


class Manager(User):
    base_role = User.Roles.MANAGER


class Developer(User):
    base_role = User.Roles.DEVELOPER
