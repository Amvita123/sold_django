from django.db import models
from users.models.user import User
from shop.models.items import ShopItem
import uuid

class Sales(models.Model):

    SALA_STATUS = (
        ('Shipped', 'Shipped'),
        ('NotShipped', 'NotShipped'),
        ('Completed', 'Completed')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_methods = models.CharField(max_length=100)
    delivery_details = models.TextField()
    payment_methods = models.CharField(max_length=100)
    final_price = models.FloatField()
    is_rated = models.BooleanField(default=False)
    sale_status = models.CharField(choices=SALA_STATUS, max_length=50, default="NotShipped")
    date_created = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, editable=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)