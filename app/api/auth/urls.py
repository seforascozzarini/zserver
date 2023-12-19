from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logoutall/', views.LogoutAllView.as_view(), name='logout-all'),
    path('reset-password/', views.PasswordResetAPIView.as_view(), name='reset-password'),
    path('otp-change-password/', views.OTPPasswordChangeAPIView.as_view(), name='otp-change-password'),
    path('change-password/', views.PasswordChangeAPIView.as_view(), name='psswd-change'),
]
