from django.conf import settings
from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class States(models.TextChoices):
        NEW = "new_task"
        ID_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_TO_RELEASE = "ready_to_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    class Priority(models.TextChoices):
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"

    title = models.CharField(max_length=200, default="New task")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    tags = models.ManyToManyField(Tag)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)
    deadline_date = models.DateTimeField(null=True)
    state = models.CharField(max_length=255, default=States.NEW, choices=States.choices)
    priority = models.CharField(
        max_length=255, default=Priority.LOW, choices=Priority.choices
    )

    def __str__(self):
        return self.title
