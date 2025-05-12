import uuid
from django.db import models
from users.models.user import User


class UserRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.FloatField()
    review = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="rating_owner")
    rated_users = models.ForeignKey(User, on_delete=models.CASCADE,related_name="rating_user")
    date_created = models.DateTimeField(auto_now_add=True)