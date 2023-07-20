"""
URL mappings for the posts API.
"""
from django.urls import path

from api.advices import views

app_name = 'advices'


urlpatterns = [
    path('create/', views.CreateAdviceView.as_view(), name='create'),
    path('get/', views.GetAdviceListView.as_view(), name='get_list'),
]