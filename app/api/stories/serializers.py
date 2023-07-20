"""
Serializers for the story API View.
"""
from rest_framework import serializers
from core.models import Story


class StoryListSerializer(serializers.ModelSerializer):
    """Serializer for the story object view/modification."""

    class Meta:
        model = Story
        fields = ['text', 'username', 'is_username_visible', 'start_date', 'end_date', 'image']


class CreateStorySerializer(serializers.ModelSerializer):
    """Serializer for the story object creation."""

    class Meta:
        model = Story
        fields = ['text', 'username', 'is_username_visible', 'start_date', 'end_date', 'image']

    def create(self, validated_data):
        """Create and return a story."""
        return Story.objects.create(**validated_data)