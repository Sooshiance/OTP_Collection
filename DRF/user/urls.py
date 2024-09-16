from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from user import views


app_name = "user"

urlpatterns = [
    path("otp/request/", views.RequestOtpAPIView.as_view(), name='otp-request'),

    path("otp/check/", views.CheckOtpAPIView.as_view(), name='otp-check'),

    path("token/refresh/", TokenRefreshView.as_view(), name='token-refresh'),
]
