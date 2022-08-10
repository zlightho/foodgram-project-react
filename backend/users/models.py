from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True, max_length=254, help_text="Почта пользователя"
    )
    first_name = models.CharField(max_length=150, help_text="Имя")
    last_name = models.CharField(max_length=150, help_text="Фамилия")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name", "username")


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_subscriber"
            )
        ]
