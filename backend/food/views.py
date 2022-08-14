from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from users.models import User

from .filters import IngredientFilter, RecipeFilter
from .models import Cart, Favorite, Ingredient, Recipe
from .permissions import RecipePermission
from .serializers import (
    GetRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    UserRecipeSerializer,
)
from .utils import get_shopping_cart_recipes, helper_model_create_delete


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
    filterset_class = RecipeFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return GetRecipeSerializer
        return RecipeSerializer

    @action(
        url_path="favorite",
        detail=True,
        methods=("DELETE", "POST"),
        permission_classes=(IsAuthenticated,),
    )
    def favorite_recipe(self, request, id):
        return helper_model_create_delete(request, Favorite, id)

    @action(
        url_path="shopping_cart",
        detail=True,
        methods=("DELETE", "POST"),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, id):
        return helper_model_create_delete(request, Cart, id)

    @action(
        url_path="download_shopping_cart",
        detail=False,
        methods=("GET",),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        shopping_list = get_shopping_cart_recipes(request)
        response = HttpResponse(
            shopping_list,
            "Content-Type: text/plain",
        )
        response[
            "Content-Disposition"
        ] = 'attachment; filename="shopping_cart.txt"'
        return response


class GetSubscribtionsViewset(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRecipeSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
