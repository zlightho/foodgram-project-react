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
from .utils import helper_model_create_delete


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
        carts = request.user.carts.all()
        shopping_dict = {}
        for cart in carts:
            for ingredient_recipe in cart.recipe.ingredientrecipe.all():
                amount = ingredient_recipe.amount
                name = ingredient_recipe.ingredient.name
                measurement_unit = (
                    ingredient_recipe.ingredient.measurement_unit
                )
                if name in shopping_dict:
                    shopping_dict[name]["amount"] += amount
                else:
                    shopping_dict[name] = {
                        "amount": amount,
                        "measurement_unit": measurement_unit,
                    }

        shopping_list = []
        for name, data in shopping_dict.items():
            shopping_list.append(
                f"{name} {data['amount']} {data['measurement_unit']}\n"
            )
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
