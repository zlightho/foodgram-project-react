from rest_framework import serializers

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "is_subscribed",
            "username",
            "first_name",
            "last_name",
            "email",
        )
        model = User

    def get_is_subscribed(self, object):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            following=object, user=request.user
        ).exists()
