from rest_framework import serializers

from .models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"
        model = User

    def get_is_subscribed(self, object):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(author=object, user=request.user)