"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models.post import Post, PostType, PetType
from core.tests.utils import create_user, create_post


class UserTests(TestCase):
    """Test User model."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test e-mail is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.type, get_user_model().UserType.ADMIN)


class PostTests(TestCase):
    """Test Post model."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
        )

    def test_create_post(self):
        """Test creating a post successful."""
        post = Post.objects.create(
            user=self.user,
            type=PostType.LOST,
            location=[12.121212, 75.343434],
            address='address',
            pet_type=PetType.CAT,
            text='text',
        )

        self.assertEqual(str(post), post.code)

    def test_generate_post_code(self):
        """Test when creating a post the correct code is generated."""
        post = create_post(user=self.user)

        self.assertIsNotNone(post.code)
        self.assertNotEqual(post.code, '')
        self.assertTrue(post.code.startswith('L'))
