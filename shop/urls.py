from django.urls import path
from shop.views import *

urlpatterns=[
    path('shop-items/', ShopItemView.as_view(), name='items'),
    path('shop-items/<uuid:item_id>/', ShopItemView.as_view(), name='items'),
    path('shop-items/<str:user_id>/', UsersItemView.as_view(), name='user-shop-items'),
    path('favorite/<uuid:item_id>/', FavoriteItemView.as_view(), name='favorite-item'),
    path('brand-details/', BrandView.as_view(), name='brand_details'),
    path('create-category/', CategoryView.as_view(), name='create_category'),
    path('sub-category/', SubCategoryView.as_view(), name='sub_category'),
    path('sub-category-items/', SubCategoryItemsView.as_view(), name='sub_category_items'),
    path('size-details/', SizeView.as_view(), name='size_details'),
    path('color-details/', ColorView.as_view(), name='color_details'),
    path('item/<uuid:item_id>/', MarkAsSoldView.as_view(), name='items_mark'),
    path('popular-item/', MostPopularItemsView.as_view(), name='popular_items'),
]