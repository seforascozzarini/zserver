"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


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
    location = ArrayField(default=list, base_field=models.FloatField())
    radius = models.PositiveIntegerField(blank=True, null=True)
    firebase_id = models.CharField(max_length=255, blank=True)
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    write_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
