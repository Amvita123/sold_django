from rest_framework import serializers
from shop.models.brand import Brand

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ('updated_at','deleted_at', 'is_deleted', 'is_active')