from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set.")
        if not email:
            raise ValueError("The Email field must be set.")

        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, password=password, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            username=username, email=email, password=password, **extra_fields
        )


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices, db_index=True
    )
    # objects = CustomUserManager()
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
