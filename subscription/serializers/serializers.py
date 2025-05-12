from rest_framework import serializers
from subscription.models.subscriptions import SubscriptionPlan, UserSubscription
from datetime import timedelta
from django.utils import timezone

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'title', 'description', 'price', 'duration', 'subscription_type', 'is_weekly']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ['plan', 'user', 'subscribe_at', 'expire_on']

        extra_kwargs = {
            'plan': {'required': True},
            'user': {'read_only': True},
            'subscribe_at': {'read_only': True},
            'expire_on': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user=request.user
        plan=validated_data['plan']
        subscribe_at = timezone.now()
        expire_on = subscribe_at + timedelta(days=plan.duration)
        return UserSubscription.objects.create(user=user, plan=plan, subscribe_at=subscribe_at, expire_on=expire_on)

