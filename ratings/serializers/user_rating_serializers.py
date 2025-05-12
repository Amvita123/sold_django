from rest_framework import serializers
from ratings.models.user_rating import UserRating
from shop.models.sales import Sales


class UserRatingSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    user_profile_pic = serializers.SerializerMethodField()
    sale_id = serializers.SerializerMethodField(required=False)
    user_id = serializers.SerializerMethodField()


    class Meta:
        model = UserRating
        fields = ['id', 'value', 'review', 'date_created', 'user_fullname', 'user_profile_pic', 'sale_id', 'user_id']
        read_only_fields = ['user_fullname', 'user_profile_pic', 'sale_id', 'user_id']

    def get_user_fullname(self, obj):
        return obj.owner.fullname.replace(' ', '').lower() if obj.owner and obj.owner.fullname else ""

    def get_user_profile_pic(self, obj):
        return obj.owner.profile_pic if obj.owner and obj.owner.profile_pic else None

    def get_sale_id(self, obj):
        sale = Sales.objects.filter(buyer=obj.owner).first()
        return str(sale.id) if sale else ""

    def get_user_id(self, obj):
        return obj.owner.id if obj.owner else ""
