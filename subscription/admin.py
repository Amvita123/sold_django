from django.contrib import admin
from subscription.models.subscriptions import UserSubscription, SubscriptionPlan

admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)

