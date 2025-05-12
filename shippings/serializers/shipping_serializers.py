from rest_framework import serializers
from shippings.models.shipping_info import ShippingInfo

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInfo
        fields = ['id', 'user', 'address', 'city', 'zip_code']