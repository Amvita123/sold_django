from django.db import models
from common.models import CommonFields


class Material(CommonFields):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name