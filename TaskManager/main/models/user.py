from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


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
