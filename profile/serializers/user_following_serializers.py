from rest_framework import serializers
from profile.models.user_following import UserFollowing


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ['following']

