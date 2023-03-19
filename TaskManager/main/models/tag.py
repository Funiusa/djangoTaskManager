import uuid
from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=30, default="v1", unique=True)
    u_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]
