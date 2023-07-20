"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import Post, Advice, Comment, CommentFlag, Item, PostFlag, PostImage, Story


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'last_name', 'first_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'type',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'create_date',
                    'write_date',
                    'last_login',
                )
            }
        ),
        (
            _('Personal data'),
            {
                'fields': (('last_name', 'first_name'),)
            }
        ),
        (
            _('Preferences'),
            {
                'fields': ('location', ('address', 'radius'), 'firebase_id')
            }
        )
    )
    readonly_fields = ['create_date', 'write_date', 'last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                'type',
                'last_name',
                'first_name',
                'location',
                'address',
                'radius',
                'firebase_id',
            )
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Define the admin pages for Posts."""
    ordering = ['-id']
    list_display = ['code', 'type', 'pet_type', 'status', 'create_date']
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'type', 'status', 'text',
                )
            }
        ),
        (
            _('User'),
            {
                'fields': (
                    'user', 'contacts',
                )
            }
        ),
        (
            _('Location'),
            {
                'fields': (
                    'address', 'location',
                )
            }
        ),
        (
            _('Pet info'),
            {
                'fields': (
                    'pet_type',
                    'pet_name',
                    'gender',
                    'age',
                    'sterilised',
                    'microchip',
                    'specific_marks',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'create_date',
                    'write_date',
                    'publish_date',
                    'close_date',
                )
            }
        ),
    )
    readonly_fields = ['create_date', 'write_date']


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PostFlag)
class PostFlagAdmin(admin.ModelAdmin):
    pass


@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(CommentFlag)
class CommentFlagAdmin(admin.ModelAdmin):
    pass

