from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AchievementViewSet, NewsViewSet, SendEmailView, LeadershipViewSet

router = DefaultRouter()
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'leadership', LeadershipViewSet, basename='leadership')

urlpatterns = [
    path('', include(router.urls)),
]
