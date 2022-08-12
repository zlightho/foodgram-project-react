from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, ReceptViewSet, GetSubscribtionsViewset

router = DefaultRouter()
router.register(r"^ingredients", IngredientViewSet)
router.register(r"^recipes", ReceptViewSet)
router.register(r"^users/subscriptions", GetSubscribtionsViewset, "users_subs")

urlpatterns = [
    path("", include(router.urls)),
]
