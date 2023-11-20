from django.urls import path, include
from rest_framework.routers import DefaultRouter

from events.views import ListViewSet, HomeAPIView, RegisterEventAPIView

app_name = 'events'

router = DefaultRouter()
router.register(r'sorted', ListViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('home/', HomeAPIView.as_view()),
    path('register/', RegisterEventAPIView.as_view()),
]