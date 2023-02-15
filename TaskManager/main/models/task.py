from django.db import models
from .user import User

""" заголовок;
    описание;
    дата создания;
    дата изменения;
    дата, до которой надо завершить задачу;
    состояние;
    приоритет. """


class Task(models.Model):
    class State(models.TextChoices):
        NEW_TASK = "new_task"
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

    title = models.ManyToManyField(User)
    description = models.TextField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)
    deadline_date = models.DateTimeField()
    state = models.CharField(
        max_length=255, default=State.NEW_TASK, choices=State.choices
    )
    priority = models.CharField(
        max_length=255, default=Priority.LOW, choices=Priority.choices
    )
