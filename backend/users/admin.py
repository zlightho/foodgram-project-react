from django.contrib import admin

from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("id", "username", "first_name", "last_name", "email")
    list_filter = ("username", "email")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    fields = ("user", "following")
