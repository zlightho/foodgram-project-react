from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Tag
from .serialisers import TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
