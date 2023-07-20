"""
Views for the user API.
"""
from rest_framework import (
    generics,
    authentication,
    permissions, status,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.users.serializers import (
    AuthTokenSerializer,
    UserCreateSerializer,
    UserManageSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserCreateSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Profile of the authenticated user."""
    serializer_class = UserManageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """Deactivate the authenticated user."""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
