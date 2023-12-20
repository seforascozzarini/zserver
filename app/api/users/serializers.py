"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis import serializers as gis_serializers

User = get_user_model()

class UserCreateSerializer(gis_serializers.GeoModelSerializer):
    """Serializer for the user object creation."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'last_name', 'first_name',
                  'location', 'address', 'radius']
        geo_field = ['location']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        validated_data['type'] = get_user_model().UserType.STANDARD
        validated_data['is_active'] = False
        return get_user_model().objects.create_user(**validated_data)


class UserManageSerializer(gis_serializers.GeoModelSerializer):
    """Serializer for the user object view/modification."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'last_name', 'first_name',
                  'location', 'address', 'radius']
        geo_field = ['location']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        read_only_fields = ['email']

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    
class ActivateUserSerializer(serializers.Serializer):
    # NOTE: DON'T CHANGE the order of these fields or the validation will fail
    user_id = serializers.IntegerField(required=True)
    token = serializers.CharField(required=True)
    
    def validate_user_id(self, value):
        try:
            self.user = User.objects.get(pk=value)
        except  User.DoesNotExist:
            raise ValidationError('not-found')
        return value
    
    def validate_token(self, value):
        if(self.user.activation_path != value):
            raise ValidationError('invalid')

