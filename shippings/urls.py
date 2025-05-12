from django.urls import path
from shippings.views import *

urlpatterns=[
    path('shipping/', ShippingView.as_view(), name='shipping'),

]