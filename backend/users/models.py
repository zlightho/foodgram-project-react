from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True, max_length=254, help_text="Почта пользователя"
    )
    first_name = models.CharField(max_length=150, help_text="Имя")
    last_name = models.CharField(max_length=150, help_text="Фамилия")
    USERNAME_FIELD = "email"
