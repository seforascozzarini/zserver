"""
URL mappings for the items API.
"""
from django.urls import path

from api.items import views

app_name = 'items'


urlpatterns = [
    path('create/', views.CreateItemView.as_view(), name='create'),
    path('get/', views.GetItemListView.as_view(), name='get_list'),
]