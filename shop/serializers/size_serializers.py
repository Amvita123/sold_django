from rest_framework import serializers
from shop.models.size import Size

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        exclude = ('updated_at','deleted_at', 'is_deleted', 'is_active')