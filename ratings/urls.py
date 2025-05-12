from django.urls import path
from ratings.views import *

urlpatterns=[
    path('rating/', UserRatingView.as_view(), name='user-rating'),
]