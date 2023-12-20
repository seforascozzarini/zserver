"""
URL mappings for the user API.
"""
from django.urls import path

from api.users import views

app_name = 'users'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('activate/', views.ActivateUserView.as_view(), name='activate'),
    path('account/', views.ProfileView.as_view(), name='account'),
]
