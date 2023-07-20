"""
Views for the comment API.
"""
from rest_framework import (
    generics,
)

from api.comments.serializers import (
    CommentListSerializer
)

from core.models import Comment


class GetCommentListView(generics.ListAPIView):
    """"Get a comment list in the system."""

    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
