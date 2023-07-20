"""
URL mappings for the stories API.
"""
from django.urls import path

from api.stories import views

app_name = 'stories'


urlpatterns = [
    path('create/', views.CreateStoryView.as_view(), name='create'),
    path('get/', views.GetStoryListView.as_view(), name='get_list'),
]