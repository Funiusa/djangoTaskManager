import uuid
from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=30, default="v1", unique=True)
    u_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.title
