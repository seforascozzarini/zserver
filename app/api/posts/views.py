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
        type = self.request.query_params.get('type')
        status = self.request.query_params.get('status')
        user_id = self.request.query_params.get('user_id')
        post_code = self.request.query_params.get('code')
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
        if user_id:
            post_list = post_list.filter(user_id=user_id)
        if post_code:
            post_list = post_list.filter(code=post_code)
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