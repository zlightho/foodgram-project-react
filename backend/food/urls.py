from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetSubscribtionsViewset, IngredientViewSet, ReceptViewSet

router = DefaultRouter()
router.register("ingredients", IngredientViewSet)
router.register("recipes", ReceptViewSet)
router.register("users/subscriptions", GetSubscribtionsViewset, "users_subs")

urlpatterns = [
    path("", include(router.urls)),
]
