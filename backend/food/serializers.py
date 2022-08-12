from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from tags.serialisers import TagSerializer
from users.serializers import UserSerializer
from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe
from tags.models import Tag
from django.db.transaction import atomic


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient", queryset=Ingredient.objects.all()
    )

    class Meta:
        fields = (
            "id",
            "amount",
        )

    def validate_amount(self, data):
        if int(data) < 1:
            raise serializers.ValidationError(
                "Количество ингредиентов в рецепте меньше одного."
            )
        return data

    def create(self, validated_data):
        return IngredientRecipe.objects.create(
            amount=validated_data.get("amount"),
            ingredient=validated_data.get("id"),
        )


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        fields = (
            "id",
            "image",
            "author",
            "ingredients",
            "tags",
            "cooking_time",
            "name",
            "text",
        )
        model = Recipe

    def bulk_create_ingredients(self, recipe, ingredients):
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    recipe=recipe,
                    amount=ingredient["amount"],
                    ingredient=ingredient["ingredient"],
                )
                for ingredient in ingredients
            ]
        )

    @atomic
    def create(self, validated_data):
        request = self.context.get("request")
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        self.bulk_create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.bulk_create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return GetRecipeSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient", read_only=True
    )
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
