from django.db import models
from users.models.user import User
from shop.models.colors import Color
from shop.models.brand import Brand
from shop.models.category import Category
from shop.models.sub_category import SubCategory
from shop.models.size import Size
from shop.models.material import Material
from django.contrib.postgres.fields import ArrayField
from common.models import CommonFields


class ShopItem(CommonFields):
    CONDITION_CHOICES = (
        ('new', 'New'),('used', 'Used'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_items')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField(default="", blank=True)
    price = models.FloatField()
    colors = models.ManyToManyField(Color, blank=False, related_name='colors_detail')
    brand = models.ManyToManyField(Brand, blank=False, related_name='brand_detail')
    is_sold = models.BooleanField(default=False)
    size = models.ManyToManyField(Size, blank=False, related_name='size_detail')
    state = models.TextField()
    category = models.ManyToManyField(Category, blank=False, related_name='category_detail')
    sub_category = models.ManyToManyField(SubCategory, blank=False, related_name='sub_category_detail')
    type = models.CharField(max_length=200)
    view_count = models.IntegerField(default=0)
    payment_methods = ArrayField(models.CharField(max_length=50))
    shipping_methods = ArrayField(models.CharField(max_length=50))
    hash_tags = ArrayField(models.CharField(max_length=50))
    material = models.ManyToManyField(Material, blank=False, related_name='material_detail')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)

    def __str__(self):
        return self.title


