from django.db import models
from common.models import CommonFields
from .category import Category


class SubCategory(CommonFields):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    translation_key = models.CharField(max_length=200, default="")
    enabled = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SubCategoryItems(CommonFields):
    name = models.CharField(max_length=50, unique=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="items")
    translation_key = models.CharField(max_length=200, default="")


    def __str__(self):
        return self.name