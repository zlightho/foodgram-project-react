from django.urls import path
from .views import FollowView

path("users/<int:pk>/subscribe/", FollowView.as_view(), name="follow"),
