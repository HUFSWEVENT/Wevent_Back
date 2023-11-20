from django.urls import path
from .views import RegisterAPIView, AuthAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path("register/", RegisterAPIView.as_view()), # post - 회원가입
    path("auth/refresh/", TokenRefreshView.as_view()),
]
# urlpatterns = [
#     path(),
# ]
