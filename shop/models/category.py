from django.db import models
from common.models import CommonFields

class Category(CommonFields):
    name = models.CharField(max_length=50, unique=True)
    translation_key = models.CharField(max_length=200, default="")
    enabled = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name