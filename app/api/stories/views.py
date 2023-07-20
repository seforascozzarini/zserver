"""
Views for the story API.
"""
from rest_framework import (
    generics,
)

from api.stories.serializers import (
    StoryListSerializer,
    CreateStorySerializer
)

from core.models import Story


class GetStoryListView(generics.ListAPIView):
    """"Get a story list in the system."""
    serializer_class = StoryListSerializer
    queryset = Story.objects.all()


class CreateStoryView(generics.CreateAPIView):
    """"Create a story in the system."""
    serializer_class = CreateStorySerializer
