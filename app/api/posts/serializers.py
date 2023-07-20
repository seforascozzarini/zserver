"""
Serializers for the post API View.
"""
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from core.models import Post


class PostCreateSerializer(gis_serializers.GeoModelSerializer):
    """Serializer for the post object creation."""

    class Meta:
        model = Post
        fields = ['code', 'type', 'location', 'address', 'pet_type',
                  'gender', 'age', 'microchip', 'sterilised',
                  'specific_marks', 'pet_name', 'text', 'contacts', 'status',
                  'default_image', 'event_date']
        geo_field = ['location']

    def create(self, validated_data):
        """Create and return a post."""
        return Post.objects.create(**validated_data)


class PostListSerializer(gis_serializers.GeoModelSerializer):
    """Serializer for the post object view/modification."""

    class Meta:
        model = Post
        fields = ['id', 'user', 'code', 'type', 'location', 'address', 'pet_type',
                  'gender', 'age', 'microchip', 'sterilised',
                  'specific_marks', 'pet_name', 'text', 'contacts', 'status',
                  'is_flagged', 'default_image', 'event_date']
        geo_field = ['location']


class PostEditSerializer(gis_serializers.GeoModelSerializer):
    """Serializer for the post object view/modification."""

    class Meta:
        model = Post
        fields = ['location', 'address', 'pet_type',
                  'gender', 'age', 'microchip', 'sterilised',
                  'specific_marks', 'pet_name', 'text', 'contacts', 'status',
                  'default_image', 'event_date']
        geo_field = ['location']

