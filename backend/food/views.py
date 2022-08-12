from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import SAFE_METHODS

from .serializers import (
    GetRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
)
from .models import Ingredient, Recipe
from .filters import IngredientFilter
from .permissions import RecipePermission


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class ReceptViewSet(ModelViewSet):
    lookup_field = "id"
    permission_classes = (RecipePermission,)
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return GetRecipeSerializer
        return RecipeSerializer
