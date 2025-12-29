from django.urls import path
from . import customer_view

urlpatterns = [
    path('', customer_view.index, name='customers-index'),
    path('register/', customer_view.RegisterView.as_view(), name='register'),
    path('login/', customer_view.LoginView.as_view(), name='login'),
    path('otp/request/', customer_view.RequestOTPView.as_view(), name='otp-request'),
    path('otp/verify/', customer_view.VerifyOTPView.as_view(), name='otp-verify'),
    path('password/reset/', customer_view.ResetPasswordView.as_view(), name='password-reset'),
    path('profile/update/', customer_view.UpdateProfileView.as_view(), name='profile-update'),
    path('profile/phone/', customer_view.UpdatePhoneView.as_view(), name='phone-update'),
]