from django.core.validators import MinValueValidator
from django.db import models
from tags.models import Tag
from users.models import User


class Ingredient(models.Model):
    measurement_unit = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    class Meta:
        constraints = (
            models.constraints.UniqueConstraint(
                fields=(
                    "measurement_unit",
                    "name",
                )
            ),
        )


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient, through="IngredientRecipe"
    )
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to="Recipe")
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField(
        validators=MinValueValidator(1, "Время приготовления меньше минуты")
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )


class IngredientRecipe(models.Model):
    amount = models.PositiveIntegerField()
    ingredient = models.ForeignKey(Ingredient, related_name="ingredientrecipe")
    recipe = models.ForeignKey(Recipe, related_name="ingredientrecipe")


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="favorites")
    recipe = models.ForeignKey(Recipe, related_name="favorites")

    class Meta:
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite"
            ),
        )


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="carts")
    recipe = models.ForeignKey(Recipe, related_name="carts")

    class Meta:
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("user", "recipe"), name="unique_cart"
            ),
        )
