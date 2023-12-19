import logging
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView, LogoutAllView as KnoxLogoutAllView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from .tasks import send_otp_pswd_reset_email
from .serializers import PasswordChangeSerializer, OTPPasswordChangeSerializer


from ..utils.exceptions import HTTPException

User = get_user_model()


api_log = logging.getLogger('zampo.api.auth')


class Authenticated(BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        base = super().authenticate_credentials(userid, password, request)
        if not base[0].is_active:
            raise exceptions.AuthenticationFailed(
                _('user__inactive'))
        return base


class LoginView(KnoxLoginView):
    authentication_classes = [Authenticated]
    permission_classes = [IsAuthenticated]

    def get_post_response_data(self, request, token, instance):
        data = super().get_post_response_data(request, token, instance)
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['type'] = request.user.type
        data['is_active'] = request.user.is_active
        return data



class LogoutView(KnoxLogoutView):
    pass


class LogoutAllView(KnoxLogoutAllView):
    pass


class PasswordResetAPIView(APIView):
    permission_classes = []
    http_method_names = ['post']

  
    def post(self, request):
        ''' Send an email to the specified user with a otp to change password '''
        try:
            self.handle_reset()
            return Response({
                'email__sent'
            })
        except HTTPException as ex:
            return ex.get_response()

    def handle_reset(self):
        email = self.request.data.get('email')
        if email is None:
            raise HTTPException('email-required.', 400)
        user = User.objects.filter(email=email)
        if not user.exists():
            raise HTTPException(
                f'user__not-found', 404)

        user = user.first()
        current_site = get_current_site(self.request)
        
        email_context = {
            'email': email,
            'domain': current_site.domain,
            'static_url': f'{current_site.domain}{settings.STATIC_URL}',
            'site_name': current_site.name,
            'protocol': 'http',
            'otp': user.get_reset_otp(expire=5),
            'expire': 5,
        }
        # send_otp_pswd_reset_email([email], email_context)
        send_otp_pswd_reset_email.apply_async(
            args=[[user.email], email_context])


class OTPPasswordChangeAPIView(APIView):
    http_method_names = ['post']
    permission_classes = []

    def post(self, request):
        ''' Change password using otp code sent to user email '''
        serializer = OTPPasswordChangeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            user.revoke_reset_otp()
            # change password
            user.set_password(serializer.validated_data['password'])
            user.force_password_change = False
            user.save()
            # logout all
            user.auth_token_set.all().delete()

            return Response('password__updated')

        except ValidationError as ve:
            return Response(ve.detail, 400)


class PasswordChangeAPIView(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ''' Change password using old password '''
        serializer = PasswordChangeSerializer(
            data=request.data, context={'user': request.user})
        try:
            serializer.is_valid(raise_exception=True)

            request.user.set_password(serializer.validated_data['password'])
            request.user.save()
            # logout all
            request.user.auth_token_set.all().delete()

            return Response({'user':request.user.id})

        except ValidationError as ve:
            return Response( 'validation__failed', 400)


