from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("id", "username", "first_name", "last_name", "email")
    list_filter = ("username", "email")
