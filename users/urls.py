from django.urls import path
from users.views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns=[
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerificationOtpView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-account/', VerifyAccountView.as_view(), name='verify-account'),
    path('request-otp/', RequestOtpView.as_view(), name='request-for-otp'),
    path('change-password/', ChangePasswordView.as_view(), name='password-change'),
    path('create-superuser/', CreateSuperUserView.as_view(), name='superuser-create'),
]