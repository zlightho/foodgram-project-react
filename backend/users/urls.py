from django.urls import path
from .views import FollowView

urlpatterns = [
    path("users/<int:pk>/subscribe/", FollowView.as_view(), name="follow"),
]
