from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path("register/", RegisterAPIView.as_view()), # post - 회원가입
    path("auth/refresh/", TokenRefreshView.as_view()),
]
# urlpatterns = [
#     path(),
# ]
