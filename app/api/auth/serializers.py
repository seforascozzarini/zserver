from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import django.contrib.auth.password_validation as validators

from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField()
    old_password = serializers.CharField()

    def validate_password(self, password):
        validators.validate_password(password)
        return password

    def validate_old_password(self, password):
        if self.context.get('user').check_password(password):
            return password
        raise ValidationError(
            'old-password__invalid')


class OTPPasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    otp = serializers.CharField()

    def validate_email(self, email):
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist as ex:
            self.user = None
            raise ValidationError('user__not-found')
        return email

    def validate_password(self, password):
        validators.validate_password(password)
        return password

    def validate_otp(self, otp):
        if self.user and self.user.check_reset_otp(otp):
            return otp
        raise ValidationError('otp__invalid')


class PostResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()