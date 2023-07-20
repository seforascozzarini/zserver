"""
URL mappings for the user API.
"""
from django.urls import path

from api.users import views

app_name = 'users'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ProfileView.as_view(), name='me'),
]
