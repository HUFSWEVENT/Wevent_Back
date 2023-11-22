from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ListViewSet, HomeAPIView, RegisterEventAPIView, EventDetailAPIView, AdDetailAPIView

app_name = 'events'

router = DefaultRouter()
router.register(r'sorted', ListViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('home/', HomeAPIView.as_view()),
    path('register/', RegisterEventAPIView.as_view()),
    path('eventDetail/<int:pk>/', EventDetailAPIView.as_view()),
    path('adDetail/<int:pk>/', AdDetailAPIView.as_view()),
]