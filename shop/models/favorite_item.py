from django.db import models
from common.models import CommonFields
from users.models.user import User
from shop.models.items import ShopItem


class FavoriteItem(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_items")
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, related_name="favorited_by_users")
