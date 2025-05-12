from django.db import models
import uuid
from users.models.user import User

class ShippingInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    address = models.TextField()
    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return self.address
