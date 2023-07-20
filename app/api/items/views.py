"""
Views for the item API.
"""
from rest_framework import (
    generics,
)

from api.items.serializers import (
    ItemListSerializer,
    ItemCreateSerializer
)

from core.models import Item


class GetItemListView(generics.ListAPIView):
    """Get a item list in the system."""

    serializer_class = ItemListSerializer
    queryset = Item.objects.all()

class CreateItemView(generics.CreateAPIView):
    """Create a item in the system."""

    serializer_class = ItemCreateSerializer