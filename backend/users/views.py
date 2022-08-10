from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .serializers import UserSerializer

from .models import Follow, User


class FollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        Follow.objects.get_or_create(user=request.user, following=user)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=201)

    def delete(self, request, pk):
        if Follow.objects.filter(user=request.user, following=pk).exists():
            Follow.objects.get(user=request.user, following=pk).delete()
            return Response("User deleted successfully", status=204)
        return Response("Error", status=400)
