from requests import request
from rest_framework import serializers

from ..tags.serialisers import TagSerializer

from ..users.serializers import UserSerializer

from .models import Ingredient, Recipe, IngredientRecipe, Cart, Favorite


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe


class RecipeSerializer(serializers.ModelSerializer):
    pass


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source="ingredient")
    name = serializers.SlugRelatedField(
        source="ingredient", slug_field="name", read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source="ingredient", slug_field="measurement_unit", read_only=True
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount", "measurement_unit", "name")


class GetRecipeSerializer(serializers.ModelSerializer):
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True, many=False)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(
        read_only=True, many=True, source="ingredientrecipe"
    )
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        exclude = ("pub_date",)

    def get_is_in_shopping_cart(self, object):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Cart.objects.filter(recipe=object, user=request.user)

    def get_is_in_favorited(self, object):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=object, user=request.user)
