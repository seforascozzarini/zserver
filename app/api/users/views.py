"""
Views for the user API.
"""
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from rest_framework import (
    generics,
    authentication,
    permissions, status, views
)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from .tasks import expire_activation_link, send_activation_email

from api.users.serializers import (
    ActivateUserSerializer,
    UserCreateSerializer,
    UserManageSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserCreateSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            headers = self.get_success_headers(serializer.data)
            self.send_activation_email(user)
            # schedule user removal if not activated
            eta = timezone.now() + timedelta(hours=settings.ACTIVATION_LINK_EXPIRE)
            expire_activation_link.apply_async(
                args=[user.pk], eta=eta)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        
    def send_activation_email(self, user):
        email_context = {
            'user': user,
            'activation_link': f'{settings.FRONTEND_URL}'
            f'{settings.FRONTEND_USER_ACTIVATION_PATH}/{user.activation_path}',
        }
        send_activation_email([user.email], email_context)
        # send_activation_email.apply_async(
        #     args=[[user.email], email_context])
        

class ActivateUserView(views.APIView):
    """Activate user account."""
    def post(self, request, *args, **kwargs):
        try:
            serializer = ActivateUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Profile of the authenticated user."""
    serializer_class = UserManageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """Deactivate the authenticated user."""
        user = self.get_object()
        # adding additional layer of security
        password = request.data.get('password', None)
        if password is None:
            return Response({'password': 'required'}, 400)
        if not user.check_password(password):
            raise Response({'password': 'invalid'}, 400)
        
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
