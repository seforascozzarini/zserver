"""
Database models.
"""
from django.contrib.gis.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password

import math
import random
from celery import current_app
from ..tasks import revoke_pswd_reset_otp
from datetime import timedelta

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.type = self.model.UserType.ADMIN
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    class UserType(models.IntegerChoices):
        STANDARD = 1, _('user_type_standard')
        PREMIUM = 2, _('user_type_premium')
        MOD = 3, _('user_type_mod')
        ADMIN = 9, _('user_type_admin')

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    type = models.SmallIntegerField(choices=UserType.choices,
                                    default=UserType.STANDARD)
    address = models.CharField(max_length=500, blank=True)
    location = models.PointField(
        geography=True, srid=4326, blank=True, null=True
    )
    radius = models.PositiveIntegerField(blank=True, null=True)
    firebase_id = models.CharField(max_length=255, blank=True)

    # one time password used for resetting password
    otp_pswd_reset = models.CharField(
        max_length=128, default=None, blank=True, null=True)


    create_date = models.DateTimeField(default=timezone.now, editable=False)
    write_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    @property
    def activation_path(self):
        ''' Return the path of the activation link built with user information '''
        infos = f'{self.pk}-{self.first_name}-{self.last_name}-{self.email}-{self.password}'
        return f'{self.id}__{urlsafe_base64_encode(infos.encode())}'

    # Reset password otp handlers
    def get_reset_otp(self, size=6, expire=5):
        '''
            Get a otp with the specified size that will be automatically deleted.
            After creation the otp will be hashed and stored inside self.otp_pswd_reset.
            args:
                - size: the length of the otp
                - expire: for how many minutes the otp will be valid 
        '''
        digits = '0123456789'
        otp = "".join([digits[math.floor(random.random() * 10)]
                      for x in range(size)])
        hashed = make_password(otp)

        # revoke deleting task if any
        if self.otp_pswd_reset is not None:
            task_id = f'{self.pk}-{self.otp_pswd_reset}'
            current_app.control.revoke(task_id)

        task_id = f'{self.pk}-{hashed}'
        eta = timezone.now() + timedelta(minutes=expire)
        revoke_pswd_reset_otp.apply_async(
            args=[self.pk], eta=eta, task_id=task_id)

        self.otp_pswd_reset = hashed
        self.save()
        return otp

    def check_reset_otp(self, otp):
        ''' Compare otp to otp_pswd_reset '''
        if self.otp_pswd_reset is not None:
            return check_password(otp, self.otp_pswd_reset)
        return False

    def revoke_reset_otp(self):
        ''' Set to null otp_pswd_reset revoking the auto-delete task '''
        if self.otp_pswd_reset is not None:
            task_id = f'{self.pk}-{self.otp_pswd_reset}'
            self.otp_pswd_reset = None
            self.save()
            current_app.control.revoke(task_id)
