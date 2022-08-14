import django_filters
from tags.models import Tag

from .models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )

    class Meta:
        fields = ("name",)
        model = Ingredient


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.NumberFilter(method="get_is_favorited")
    is_in_shopping_cart = django_filters.NumberFilter(
        method="get_is_in_shopping_cart"
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )

    class Meta:
        model = Recipe
        fields = ("tags", "author", "is_favorited", "is_in_shopping_cart")

    def get_is_favorited(self, queryset, name, value):
        if value == 1 and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value == 1 and not self.request.user.is_anonymous:
            return queryset.filter(carts__user=self.request.user)
        return queryset
