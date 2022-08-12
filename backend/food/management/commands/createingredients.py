import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from food.models import Ingredient

FILES = os.path.join(settings.BASE_DIR, "data/ingredients.json")


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(FILES) as file:
            data = json.load(file)
        for ingredient in data:
            Ingredient.objects.get_or_create(**ingredient)
