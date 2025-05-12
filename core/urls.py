from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('items/', include('shop.urls')),
    path('sub/', include('subscription.urls')),
    path('pre/', include('preferences.urls')),
    path('shipping/', include('shippings.urls')),
    path('profile/', include('profile.urls')),
    path('froum/', include('froum.urls')),
    path('search/', include('search.urls')),
    path('ratings/', include('ratings.urls')),
    path('cms/', include('cms.urls')),
    path('others/', include('others.urls')),
]
