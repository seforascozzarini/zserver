"""
Views for the post API.
"""
from rest_framework import (
    generics,
    authentication,
    permissions, status,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.posts.serializers import (
    PostCreateSerializer,
    PostListSerializer
)

from core.models import Post

from core.models.post import PostStatus


class CreatePostView(generics.CreateAPIView):
    """Create a new post in the system."""
    serializer_class = PostCreateSerializer


class GetPostListView(generics.ListAPIView):
    """"Get a post list in the system."""

    serializer_class = PostListSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        user_id = self.request.query_params.get('user_id')
        post_code = self.request.query_params.get('code')
        post_type = self.request.query_params.get('post_type')
        status = self.request.query_params.get('status')

        post_list = post_list.filter(status=status) if status else Post.objects.all()

        if user_id:
            post_list = post_list.filter(user_id=user_id)
        if post_code:
            post_list = post_list.filter(code=post_code)
        if post_type:
            post_list = post_list.filter(type=post_type)
        if id:
            post_list = post_list.filter(id=id)

        return post_list


class GetPostByText(generics.ListAPIView):
    """"Get a post list filtered by text in the system."""
    http_method_names = ['get']
    serializer_class = PostListSerializer

    def get_queryset(self):
        text_to_search = self.request.query_params.get('text')
        post_list = None
        if Post.objects.filter(type=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(location=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(pet_type=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(gender=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(age=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(microchip=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(sterilised=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(specifics_marks=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(pet_name=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(text=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(contacts=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(status=text_to_search):
            post_list.append(Post)
        if Post.objects.filter(event_date=text_to_search):
            post_list.append(Post)

        return post_list
