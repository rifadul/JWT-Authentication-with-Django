from django.contrib import admin
from django.urls import path
from account.views import UserChangePasswordView, UserProfileView, UserRegistrationView,UserLoginView,SendPasswordResetEmailView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(),name='registration'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('password-change/', UserChangePasswordView.as_view(),name='password-change'),
    path('sent-reset-password-email/', SendPasswordResetEmailView.as_view(),name='sent-reset-password-email'),
]