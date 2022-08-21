from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe


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
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        "author",
        "name",
        "image",
        "text",
        "cooking_time",
    )
    list_display = ("author", "name", "count_favorites")
    filter_horizontal = ("tags",)
    inlines = (IngredientInline, TagInline)
    list_filter = ("author", "name", "tags")
    search_fields = ("author", "name", "tags")

    @admin.display()
    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    fields = ("amount", "ingredient", "recipe")
