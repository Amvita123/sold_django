from django.db import models
from common.models import CommonFields

class Color(CommonFields):
    name = models.CharField(max_length=50, unique=True)
    translation_key = models.CharField(max_length=200, default="")
    color_code = models.CharField(max_length=6, null=True, blank=True)



    def __str__(self):
        return self.name