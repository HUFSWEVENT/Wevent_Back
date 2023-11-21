from django.urls import path
from .views import RegisterAPIView, AuthAPIView, EmailAuthAPIView, TokenRefreshAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("auth/", AuthAPIView.as_view()),
    path("auth/refresh/", TokenRefreshAPIView.as_view()),
    path("auth/email/", EmailAuthAPIView.as_view()),
]