from rest_framework.response import Response
from django.db.models.aggregates import Sum

from .models import IngredientRecipe, Recipe
from .serializers import RecipeShortSerializer


def helper_model_create_delete(request, model, pk):
    if pk is None or not Recipe.objects.filter(id=pk).exists():
        return Response("Отсутствует данный рецепт", status=404)
    recipe = Recipe.objects.get(id=pk)
    if request.method.lower() == "delete":
        model.objects.get(user=request.user, recipe=recipe)
        return Response(status=204)
    model.objects.get_or_create(user=request.user, recipe=recipe)
    return Response(RecipeShortSerializer(recipe, many=False).data, status=201)


def get_shopping_cart_recipes(request):
    shopping_items = (
        IngredientRecipe.objects.annotate(
            _sum=Sum("ingredient__ingredientrecipe__amount")
        )
        .values("_sum", "ingredient__name", "ingredient__measurement_unit")
        .filter(recipe__carts__user=request.user)
    )
    shopping_list = []
    for item in shopping_items:
        shopping_list.append(
            f"{item['ingredient__name']} {item['_sum']}"
            f" {item['ingredient__measurement_unit']}"
        )
    return set(shopping_list)
