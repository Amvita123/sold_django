from django.urls import path
from cms.views import *

urlpatterns=[
    path('cms/', CmsView.as_view(), name='cms_view'),
]