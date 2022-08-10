from colorfield.fields import ColorField
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(unique=True)
    slug = models.SlugField(
        unique=True,
        validators=[
            RegexValidator(
                r"^[-a-zA-Z0-9_]+$",
                message="Slug может содержать латинские буквы, цифры и знак _",
            )
        ],
    )
