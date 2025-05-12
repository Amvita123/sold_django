from django.urls import path
from profile.views import *

urlpatterns=[
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<uuid:user_id>/', UserFollowView.as_view(), name='follow_user'),
    path('user/<uuid:user_id>/', ProfileByIdView.as_view(), name='user_by_id'),
    path('follower/', FollowersView.as_view(), name='get_followers'),
    path('following/', FollowingView.as_view(), name='get_following'),

]