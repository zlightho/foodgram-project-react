from django.contrib import admin

from .models import IngredientRecipe, Recipe, Ingredient, Favorite, Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = ("recipe", "user")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = ("recipe", "user")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = ("name", "measurement_unit")
    list_filter = ("name",)


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ("author", "name", "image", "text", "cooking_time")
    list_display = ("author", "name")
    filter_horizontal = ("tags",)
    inlines = (IngredientInline, TagInline)
    list_filter = ("author", "name", "tags")
