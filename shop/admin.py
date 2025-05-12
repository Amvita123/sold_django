from django.contrib import admin
from .models.brand import Brand
from .models.category import Category
from .models.items import ShopItem
from .models.material import Material
from .models.sub_category import SubCategory
from .models.colors import Color
from .models.size import Size

admin.site.register(ShopItem)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Material)
admin.site.register(Size)
admin.site.register(SubCategory)
