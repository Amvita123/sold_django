from django.db import models
from common.models import CommonFields

class Brand(CommonFields):
    name = models.CharField(max_length=50, unique=True)
    enabled = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name