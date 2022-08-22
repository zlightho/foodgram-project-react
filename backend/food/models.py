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
                ),
                name="Ингредиенты",
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
        validators=(MinValueValidator(1, "Время приготовления меньше минуты"),)
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-pub_date",)

    # def clean(self):
    #     validated_ingredients = []
    #     for ingredient in self.ingredients:
    #         if ingredient. in validated_ingredients:
    #             raise models.ValidationError(
    #                 "Ингредиенты не должны повторяться"
    #             )
    #         validated_ingredients.append(ingredient.ingredient.id)


class IngredientRecipe(models.Model):
    amount = models.PositiveIntegerField()
    ingredient = models.ForeignKey(
        Ingredient, related_name="ingredientrecipe", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="ingredientrecipe", on_delete=models.CASCADE
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User, related_name="favorites", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="favorites", on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite"
            ),
        )


class Cart(models.Model):
    user = models.ForeignKey(
        User, related_name="carts", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="carts", on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("user", "recipe"), name="unique_cart"
            ),
        )
