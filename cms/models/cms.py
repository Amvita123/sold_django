from django.db import models
import uuid

class Cms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=300)
    content = models.JSONField(default=dict)

    def __str__(self):
        return self.slug