"""
Utilities for tests.
"""
from django.contrib.auth import get_user_model

from core.models import Post
from core.models.post import PostType, PetType


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_post(user, **params):
    """Create and return a new post."""
    defaults = {
        'type': PostType.LOST,
        'location': [12.121212, 75.343434],
        'address': 'address',
        'pet_type': PetType.CAT,
        'text': 'text',
    }
    defaults.update(params)
    return Post.objects.create(user=user, **defaults)
