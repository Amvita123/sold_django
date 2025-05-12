from django.db import models
import uuid
from users.models.user import User

class SubscriptionPlan(models.Model):
    SUBSCRIPTION_CHOICE = (('FEATURED_DRESSING', 'FEATURED_DRESSING'),
                           ('SELLER', 'SELLER'),
                           ('TRENDING_SEARCH', 'TRENDING_SEARCH'),
                           ('BOOSTED_VISIBILITY', 'BOOSTED_VISIBILITY'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    duration = models.PositiveIntegerField()
    subscription_type = models.CharField(max_length= 200, choices=SUBSCRIPTION_CHOICE)
    is_weekly = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='plan_details')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_details')
    subscribe_at = models.DateTimeField(auto_now_add=True)
    expire_on = models.DateTimeField()


