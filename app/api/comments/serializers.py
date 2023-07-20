"""
Serializers for the comment API View.
"""
from rest_framework import serializers
from core.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    """Serializer for the comment object view/modification."""

    class Meta:
        model = Comment
        fields = ['post_id', 'user_id', 'text', 'upvote', 'downvote']