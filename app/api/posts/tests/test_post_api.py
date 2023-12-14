"""
Tests for the post API.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Post
from core.tests.utils import create_user

CREATE_POST_URL = reverse('api:posts:create')
GET_POST_LIST_URL = reverse('api:posts:get_list')

def create_post(**params):
    """Create and return a new post."""
    return Post.objects.create(**params)

#
# class PrivatePostApiTest(TestCase):
#     """Test the private features of the post API."""
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_create_post_success(self):
#         """Test creating a post is successful."""
#         payload = {
#             'type': 1,
#             'address': 'Via Borgo Visignolo 56, Baiso',
#             'pet_type': 1,
#             'gender': 1,
#             'age': 5,
#             'microchip': 1,
#             'sterilised': 1,
#             'specific_marks': 'Macchia rossa',
#             'pet_name': 'Simba',
#             'text': 'Ho perso il gatto',
#             'contacts': 'sefora.scozzarini@gmail.com',
#             'status': 1,
#
#         }
#         res = self.client.post(CREATE_POST_URL, payload, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#
#     def test_create_post_with_location_success(self):
#         """Test creating a post is successful."""
#         payload = {
#             'type': 1,
#             'location': {
#                 'type': 'Point',
#                 'coordinates': [
#                     12.972112,
#                     77.593321
#                 ]
#             },
#             'address': 'Via Borgo Visignolo 56, Baiso',
#             'pet_type': 1,
#             'gender': 1,
#             'age': 5,
#             'microchip': 1,
#             'sterilised': 1,
#             'specific_marks': 'Macchia rossa',
#             'pet_name': 'Simba',
#             'text': 'Ho perso il gatto',
#             'contacts': 'sefora.scozzarini@gmail.com',
#             'status': 1,
#
#         }
#         res = self.client.post(CREATE_POST_URL, payload, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         user = get_user_model().objects.get(email=payload['email'])
#         point = Point(*payload['location']['coordinates'])
#         self.assertTrue(user.location.equals(point))


class PublicPostApiTest(TestCase):
    """Test the public features of the post API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Mario',
            last_name='Rossi'
        )

    def test_get_post_list(self):
        """Test for get post list"""
        post = create_post(
            type=1,
            pet_type=1,
            address='Via Matteotti, 56,',
            text='ho perso il gatto',
            location=[44.702112,10.563321],
            user_id=self.user.id

        )

        res = self.client.get(GET_POST_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], post.id)
