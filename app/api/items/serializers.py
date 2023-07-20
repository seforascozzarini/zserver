"""
Serializers for the item API View.
"""
from rest_framework import serializers
from core.models import Item


class ItemListSerializer(serializers.ModelSerializer):
    """Serializer for the item object view/modification."""

    class Meta:
        model = Item
        fields = ['name', 'price', 'image', 'type']


class ItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for the item object creation."""

    class Meta:
        model = Item
        fields = ['name', 'price', 'image', 'type']

    def create(self, validated_data):
        """Create and return an item."""
        return Item.objects.create(**validated_data)