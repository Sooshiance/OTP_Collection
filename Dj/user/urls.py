from django.urls import path 

from .views import *


app_name = "user"

urlpatterns = [
    path('', loginUser, name='LOGIN'),
    path('otp-login-valid/', otpLoginValidation, name='OTP-LOGIN-VERIFY'),
    path('profile/', userProfile, name='PROFILE'),
    path('logout/', logoutUser, name='LOGOUT'),
    
    path('register/', registerUser, name='REGISTER'),
    path('otp-register-valid/', otpRegisterValidation, name='OTP-REGISTER-VERIFY'),
    
    path('reset-password/', otpPassworReset, name='FORGET'),
    path('otp-password-reset/', checkOTP, name='RESET'),
    path('confirm-password/', confirmResetPassowrd, name='CONFIRM'),
]
