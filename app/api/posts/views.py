"""
Views for the post API.
"""
from rest_framework import (
    views, mixins,
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
from django.contrib.gis.geos import Point

from api.posts.serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostImageListSerializer,
    PostImageCreateSerializer
)


from rest_framework.pagination import PageNumberPagination


from core.models import Post, PostImage
from core.models.post import PostStatus

from ..utils.query_filters import filterby_boolean_param, filterby_or_list_param
from ..utils.exceptions import HTTPException


class CreatePostView(generics.CreateAPIView):
    """Create a new post in the system."""
    serializer_class = PostCreateSerializer




class GetPostListView(generics.GenericAPIView):
    """
    Get a post list in the system.
        
        The following query parameters can be used to filter the list:
            - search[:str]: search for a post against the following fields: pet_name, text, contacts and specific marks
            - type[:str]: filter by type
            - pet_type[:list<int>] filter by pet type
            - microchiped[:list<int>]: filter by microchiped
            - sterilized[:list<int>]: filter by sterilized
            - gender[:list<int>]: filter by gender
            - pet_type[:list<int>]: filter by pet_type
            - status[:list<int>]: filter by status NOTE: draft posts are only visible to the user that created them
            - related_to[:int]: filter by related post (possible matches)
            
        - Position and distance:
            - latitude[:float]: latitude of the position
            - longitude[:float]: longitude of the position
            - distance__gte[:int]: minimum distance from the position
            - distance__lte[:int]: maximum distance from the position
            NOTE: latitude, longitude and distance (lte or gte) are required together unless the user is authenticated
                and the location considered is the user location and the radius is the user radius (unless distance is specified)
    """

    serializer_class = PostListSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
        except HTTPException as e:
            return e.get_response()
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        self.pagination_class.page_size_query_param = 'page_size'
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        related_id = self.request.query_params.get('related_to')
        if related_id is not None:
            related = Post.objects.get(related_id)
            if related.status == PostStatus.DRAFT:
                return Post.objects.none()
            qs = Post.objects.get_related(related)
        else:
            status = self.request.query_params.get('status', 1)
            if status == 0:
                if self.request.user.is_authenticated:
                    qs = Post.objects.filter(user=self.request.user)
                else: 
                    return Post.objects.none()
            qs = Post.objects.all().filter(status)
        
        search = self.request.query_params.get('search')
        if search is not None:
            qs = qs.search(search)
        
                    
        qs = filterby_or_list_param(qs, self.request, 'type')
        qs = filterby_or_list_param(qs, self.request, 'pet_type')
        qs = filterby_or_list_param(qs, self.request, 'gender')
        qs = filterby_or_list_param(qs, self.request, 'sterilized')
        qs = filterby_or_list_param(qs, self.request, 'microchiped')
        
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        distance__gte = self.request.query_params.get('distance__gte', None)
        distance__lte = self.request.query_params.get('distance__lte', None)
        
        if latitude is not None and longitude is not None:
            if (distance__gte is not None or distance__lte is not None):
                try:
                    location = Point(float(longitude), float(latitude))
                except Exception:
                    raise HTTPException(400, {'latitude': 'invalid', 'longitude': 'invalid'})
                qs = qs.annotate_distance(location)
                if distance__gte is not None:
                    qs = qs.filter(distance__gte=distance__gte)
                if distance__lte is not None: 
                    qs = qs.filter(distance__lte=distance__lte)
            else:
                raise HTTPException(400, {'distance': 'required'})
        elif self.user.is_authenticated:
            if (distance__gte is not None or distance__lte is not None):
                qs = qs.annotate_distance(self.user.location)
                if distance__gte is not None:
                    qs = qs.filter(distance__gte=distance__gte)
                if distance__lte is not None:
                    qs = qs.filter(distance__lte=distance__lte)
            else:    
                qs = qs.filterby_user_location(self.user)


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