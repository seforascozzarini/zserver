"""
URL mappings for the posts API.
"""
from django.urls import path

from api.posts import views

app_name = 'posts'


urlpatterns = [
    path('create/', views.CreatePostView.as_view(), name='create'),
    path('get/', views.GetPostListView.as_view(), name='get_list'),
    path('get_posts_by/', views.GetPostByText.as_view(), name='get_post_by'),
]
