import uuid
from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=30, default="v1")
    u_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title
