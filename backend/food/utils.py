from .models import Recipe
from rest_framework.response import Response
from .serializers import RecipeShortSerializer


def helper_model_create_delete(request, model, pk):
    if pk is None or not Recipe.objects.filter(id=pk).exists():
        return Response("Отсутствует данный рецепт", status=404)
    recipe = Recipe.objects.get(id=pk)
    if request.method.lower() == "delete":
        model.objects.get(user=request.user, recipe=recipe)
        return Response(status=204)
    model.object.get_or_create(user=request.user, recipe=recipe)
    return Response(RecipeShortSerializer(recipe, many=False).data, status=201)
