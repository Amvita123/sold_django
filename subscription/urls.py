from django.urls import path
from subscription.views import *

urlpatterns=[
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('user_subscription/', UserSubscriptionView.as_view(), name='user_subscription'),
]