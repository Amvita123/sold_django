from django.db import models

class Preference(models.Model):
    show_location = models.BooleanField(default=True)
    show_notification = models.BooleanField(default=True)
    holiday_mode = models.BooleanField(default=False)

    class Meta:
        abstract = True
