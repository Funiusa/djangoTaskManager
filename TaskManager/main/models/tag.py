import uuid

from django.db import models
from .task import Task


class Tag(models.Model):
    title = models.ManyToManyField(Task)
    u_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
