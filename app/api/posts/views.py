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
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from api.posts.serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostImageListSerializer,
    PostImageCreateSerializer
)

from core.models import Post, PostImage

from core.models.post import PostStatus


class CreatePostView(generics.CreateAPIView):
    """Create a new post in the system."""
    serializer_class = PostCreateSerializer


class GetPostListView(generics.ListAPIView):
    """"Get a post list in the system."""

    serializer_class = PostListSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        type = self.request.query_params.get('type')
        status = self.request.query_params.get('status')
        user = self.request.query_params.get('user')
        code = self.request.query_params.get('code')
        pet_type = self.request.query_params.get('pet_type')
        gender = self.request.query_params.get('gender')
        microchip = self.request.query_params.get('microchip')
        sterilised = self.request.query_params.get('sterilised')
        location = self.request.query_params.get('location')
        address = self.request.query_params.get('address')
        age = self.request.query_params.get('age')
        specific_marks = self.request.query_params.get('specific_marks')
        pet_name = self.request.query_params.get('pet_name')
        text = self.request.query_params.get('text')
        contacts = self.request.query_params.get('contacts')
        event_date = self.request.query_params.get('event_date')

        post_list = Post.objects.all()
        post_list = post_list.filter(status=status) if status else Post.objects.all()

        if id:
            post_list = post_list.filter(id=id)
        if type:
            post_list = post_list.filter(type=type)
        if user:
            post_list = post_list.filter(user=user)
        if code:
            post_list = post_list.filter(code=code)
        if pet_type:
            post_list = post_list.filter(pet_type=pet_type)
        if gender:
            post_list = post_list.filter(gender=gender)
        if microchip:
            post_list = post_list.filter(microchip=microchip)
        if sterilised:
            post_list = post_list.filter(sterilised=sterilised)
        if location:
            post_list = post_list.filter(location=location)
            # post_list = GeometryFilter(name='location', lookup_expr='location')

            # radius = 2000
            # location = Point(location.coordinates[0], location.coordinates[1], srid=4326)
            # post_list = Post.objects.filter(
            #     location__distance_lte=(
            #         location,
            #         D(m=radius)
            #     )
            # ).distance(
            #     location
            # ).order_by(
            #     'distance'
            # )
        if address:
            post_list = post_list.filter(address=address)
        if age:
            post_list = post_list.filter(age=age)
        if specific_marks:
            post_list = post_list.filter(specific_marks=specific_marks)
        if pet_name:
            post_list = post_list.filter(pet_name=pet_name)
        if text:
            post_list = post_list.filter(text=text)
        if contacts:
            post_list = post_list.filter(contacts=contacts)
        if event_date:
            post_list = post_list.filter(event_date=event_date)

        if pet_type and type:
            post_list = post_list.filter(pet_type=pet_type).filter(type=type)

        return post_list


class CreatePostImageView(generics.CreateAPIView):
    """Create a new postImage in the system."""
    serializer_class = PostImageCreateSerializer


class GetPostImageListView(generics.ListAPIView):
    """"Get a post image list in the system."""

    serializer_class = PostImageListSerializer

    def get_queryset(self):
        post = self.request.query_params.get('post')
        is_default = self.request.query_params.get('is_default')
        image = self.request.query_params.get('image')
        description = self.request.query_params.get('description')

        post_image_list = PostImage.objects.all()

        if post:
            post_image_list = post_image_list.filter(post=post)
        if is_default:
            post_image_list = post_image_list.filter(is_default=is_default)
        if image:
            post_image_list = post_image_list.filter(image=image)
        if description:
            post_image_list = post_image_list.filter(description=description)

        return post_image_list


# TODO AGGIUNGERE RICERCA DELLA DISTANZA DA UN PUNTO
class GetPostLocation(generics.ListAPIView):
    """Get a post list filtered by location in the system."""
    http_method_names = ['get']
    serializer_class = PostListSerializer

    def get_queryset(self):
        location = self.request.query_params.get('location')
        longitude = self.request.query_params.get('longitude')
        latitude = self.request.query_params.get('latitude')
        radius = self.request.query_params.get('radius')

        location = Point(longitude, latitude)

        queryset = Post.objects.filter(location__distance_lte=(location, D(m=location.distance))).distance(location).order_by('distance')

        return queryset