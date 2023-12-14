"""
Serializers for the post API View.
"""
from rest_framework import serializers

from core.models import Post, PostImage


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for the post object creation."""

    class Meta:
        model = Post
        fields = ['user', 'type', 'location', 'address', 'pet_type',
                  'gender', 'age', 'microchip', 'sterilised',
                  'specific_marks', 'pet_name', 'text', 'contacts', 'status',
                  'default_image', 'event_date']

    def create(self, validated_data):
        """Create and return a post."""
        return Post.objects.create(**validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for the post object view/modification."""

    class Meta:
        model = Post
        fields = ['id', 'user', 'code', 'type', 'location', 'address', 'pet_type',
                  'gender', 'age', 'microchip', 'sterilised',
                  'specific_marks', 'pet_name', 'text', 'contacts', 'status',
                  'is_flagged', 'default_image', 'event_date']


class PostEditSerializer(serializers.ModelSerializer):
    """Serializer for the post object view/modification."""

    class Meta:
        model = Post
        fields = ['location', 'address', 'pet_type',
                  'gender', 'age', 'microchip', 'sterilised',
                  'specific_marks', 'pet_name', 'text', 'contacts', 'status',
                  'default_image', 'event_date']


class PostImageCreateSerializer(serializers.ModelSerializer):
    """Serializer for the post image object creation."""

    class Meta:
        model = PostImage
        fields = ['post', 'is_default', 'image', 'description']

    def create(self, validated_data):
        """Create and return a post."""
        return Post.objects.create(**validated_data)


class PostImageListSerializer(serializers.ModelSerializer):
    """Serializer for the post image object creation."""

    class Meta:
        model = PostImage
        fields = ['post', 'is_default', 'image', 'description']