"""
URL mappings for the comment API.
"""
from django.urls import path

from api.comments import views

app_name = 'comments'


urlpatterns = [
    path('get/', views.GetCommentListView.as_view(), name='get_list'),
]