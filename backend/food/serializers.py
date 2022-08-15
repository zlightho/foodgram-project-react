from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from tags.models import Tag
from tags.serialisers import TagSerializer
from users.models import Follow, User
from users.serializers import UserSerializer
from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe


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
        model = IngredientRecipe
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
    ingredients = IngredientInRecipeSerializer(many=True)
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

    def validate(self, data):
        validated_ingredients = []
        for ingredient in data.get("ingredients"):
            if ingredient["amount"] < 1:
                raise serializers.ValidationError("Меньше одного ингредиента")
            if ingredient in validated_ingredients:
                raise serializers.ValidationError(
                    "Ингредиенты не должны повторяться"
                )
            validated_ingredients.append(ingredient)
        if int(data.get("cooking_time")) < 1:
            raise serializers.ValidationError(
                "Время приготовления меньше минуты"
            )
        if len(validated_ingredients) < 1:
            raise serializers.ValidationError("Не переданы ингредиенты")
        if len(data.get("tags")) < 1:
            raise serializers.ValidationError("Не переданы тэги")
        return data

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
        model = Recipe
        exclude = ("pub_date",)

    def get_is_in_shopping_cart(self, object):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Cart.objects.filter(recipe=object, user=request.user).exists()

    def get_is_favorited(self, object):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            recipe=object, user=request.user
        ).exists()


class UserRecipeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source="recipes__count")
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "recipes",
            "recipes_count",
            "is_subscribed",
        )
        read_only_fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "recipes",
            "recipes_count",
            "is_subscribed",
        )

    def get_recipes(self, obj):
        request = self.context.get("request")
        try:
            limit = int(
                request.parser_context.get("request").GET.get("recipes_limit")
            )
        except AttributeError:
            limit = None
        except TypeError:
            limit = None
        if limit is None:
            recipes = obj.recipes.all()
        else:
            recipes = obj.recipes.all()[:limit]
        return RecipeShortSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            following__id=obj.id, user=request.user
        ).exists()
