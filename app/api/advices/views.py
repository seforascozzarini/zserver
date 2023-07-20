"""
Views for the advice API.
"""
from rest_framework import (
    generics,
)
from api.advices.serializers import (
    AdviceListSerializer,
    AdviceCreateSerializer
)

from core.models import Advice


class GetAdviceListView(generics.ListAPIView):
    """Get a advice list in the system."""
    serializer_class = AdviceListSerializer
    queryset = Advice.objects.all()

class CreateAdviceView(generics.CreateAPIView):
    """Create an advice in the system."""
    serializer_class = AdviceCreateSerializer