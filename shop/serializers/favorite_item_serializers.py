from rest_framework import serializers
from shop.models.favorite_item import FavoriteItem

class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = ['item']