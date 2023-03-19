from django.db import models
from .user import User, Developer
from .tag import Tag


class Task(models.Model):
    class States(models.TextChoices):
        NEW = "new_task"
        IN_DEVELOPMENT = "in_development"
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
    assigned_to = models.ManyToManyField(
        Developer,
        verbose_name="Executor",
        related_name="tasks_assigned_to",
        related_query_name="assigned_tasks",
        blank=True,
        limit_choices_to={
            "role": User.Roles.DEVELOPER,
        },
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Author",
        related_name="tasks_assigned_by",
        limit_choices_to={"role__in": [User.Roles.MANAGER, User.Roles.ADMIN]},
    )
    tags = models.ManyToManyField(Tag)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)
    deadline_date = models.DateTimeField(null=True)
    state = models.CharField(max_length=255, default=States.NEW, choices=States.choices)
    priority = models.CharField(
        max_length=255, default=Priority.LOW, choices=Priority.choices
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]
