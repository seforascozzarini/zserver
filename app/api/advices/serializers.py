"""
Serializers for the advice API View.
"""
from rest_framework import serializers

from core.models import Advice


class AdviceListSerializer(serializers.ModelSerializer):
    """Serializer for the advice object view/modification."""

    class Meta:
        model = Advice
        fields = ['id', 'title', 'text']


class AdviceCreateSerializer(serializers.ModelSerializer):
    """Serializer for the advice object creation."""

    class Meta:
        model = Advice
        fields = ['title', 'text']

    def create(self, validated_data):
        """Create and return an advice."""
        return Advice.objects.create(**validated_data)

