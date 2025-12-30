from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='customers-index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('otp/request/', views.RequestOTPView.as_view(), name='otp-request'),
    path('otp/verify/', views.VerifyOTPView.as_view(), name='otp-verify'),
    path('password/reset/', views.ResetPasswordView.as_view(), name='password-reset'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='profile-update'),
    path('profile/phone/', views.UpdatePhoneView.as_view(), name='phone-update'),
]