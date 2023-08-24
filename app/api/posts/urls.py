"""
URL mappings for the posts API.
"""
from django.urls import path

from api.posts import views

app_name = 'posts'


urlpatterns = [
    path('create/', views.CreatePostView.as_view(), name='create'),
    path('create_post_image/', views.CreatePostImageView.as_view(), name='create'),
    path('get/', views.GetPostListView.as_view(), name='get_list'),
    path('get_post_image/', views.GetPostImageListView.as_view(), name='get_list'),


]
