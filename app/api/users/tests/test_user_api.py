"""
Tests for the user API.
"""
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.utils import create_user

CREATE_USER_URL = reverse('api:users:create')
TOKEN_URL = reverse('api:users:token')
ME_URL = reverse('api:users:me')


class PublicUserApiTest(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Mario',
            'last_name': 'Rossi',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertEqual(user.first_name, payload['first_name'])
        self.assertEqual(user.last_name, payload['last_name'])

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Mario',
            'last_name': 'Rossi',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 8 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'first_name': 'Mario',
            'last_name': 'Rossi',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        )
        self.assertFalse(user_exists)

    def test_create_user_with_location_success(self):
        """Test creating a User with location data."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'location': {
                'type': 'Point',
                'coordinates': [
                    12.972112,
                    77.593321
                ]
            }
        }
        res = self.client.post(CREATE_USER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        point = Point(*payload['location']['coordinates'])
        self.assertTrue(user.location.equals(point))

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Mario',
            'last_name': 'Rossi',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')

        payload = {
            'email': 'test@example.com',
            'password': 'badpass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manage_user_unauthorized(self):
        """Test authentication is required for managing user profile."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.put(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.patch(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.delete(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Mario',
            last_name='Rossi'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'type': self.user.type,
            'location': self.user.location,
            'address': self.user.address,
            'radius': self.user.radius,
            'firebase_id': self.user.firebase_id,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'first_name': 'Gianni', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))

    def test_update_email_not_allowed(self):
        """Test updating the user e-mail does not apply changes."""
        payload = {'email': 'another@example.com'}
        original_email = self.user.email
        res = self.client.patch(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, original_email)

    def test_delete_account(self):
        """Test account deactivation by authenticated user."""
        res = self.client.delete(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
