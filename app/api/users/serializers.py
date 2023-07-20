"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers


class UserCreateSerializer(gis_serializers.GeoModelSerializer):
    """Serializer for the user object creation."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class UserManageSerializer(gis_serializers.GeoModelSerializer):
    """Serializer for the user object view/modification."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'last_name', 'first_name', 'type',
                  'location', 'address', 'radius', 'firebase_id']
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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField(
        write_only=True,
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
