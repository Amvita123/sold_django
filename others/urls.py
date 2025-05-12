from django.urls import path
from others.views import *

urlpatterns=[
    path('report/', UserReportView.as_view(), name='user-report'),
]