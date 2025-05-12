import uuid
from django.db import models
from users.models.user import User


class UserReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reason = models.CharField(max_length=500)
    description = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    report_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_report_by')
    report_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_report_to')