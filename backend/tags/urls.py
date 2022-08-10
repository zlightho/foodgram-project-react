from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Tag
from .views import TagViewSet


router = DefaultRouter()
router.register(r"^tags", TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
