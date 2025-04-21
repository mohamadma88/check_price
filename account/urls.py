from django.urls import path
from .views import OtpVerificationView, UserLoginView, ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'account'
urlpatterns = [
    path('register', UserLoginView.as_view(), name='register'),
    path('otp', OtpVerificationView.as_view(), name='otp'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', ProfileView.as_view(), name='profile'),

]
