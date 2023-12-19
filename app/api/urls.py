"""
URL mappings for the API.
"""
from django.urls import path, include

app_name = 'api'


urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('users/', include('api.users.urls')),
    path('posts/', include('api.posts.urls')),
    path('advices/', include('api.advices.urls')),
    path('items/', include('api.items.urls')),
    path('stories/', include('api.stories.urls')),
    path('comments/', include('api.comments.urls')),
]
