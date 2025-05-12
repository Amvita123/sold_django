from rest_framework import serializers
from shop.models.colors import Color

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        exclude = ('created_at', 'updated_at','deleted_at', 'is_deleted', 'is_active')