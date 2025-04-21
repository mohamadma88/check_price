from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from unittest.mock import patch
from account.models import Otp, Profile, User


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('account:register')

    @patch('account.views.random.randint')
    def test_send_otp(self, mock_randint):
        mock_randint.return_value = 123456

        data = {
            'phone': '11223344556'
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": "otp has been sent to your phone"})
        otp_exists = Otp.objects.filter(phone='11223344556', code=123456).exists()
        self.assertTrue(otp_exists)

    def test_invalid_phone(self):
        data = {
            'phone': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone='11223344556', password='1111')
        cls.profile = Profile.objects.create(phone=cls.user, name='mohamad', last_name='mmm', birthday='2000-12-22',
                                             melicode='2233441155', bank='1122334455667788')


def test_profile_not_found(self):
    self.profile.delete()

    url = reverse('account:profile')
    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


def test_post_profile_create(self):
    url = reverse('account:profile')
    data = {
        'phone': self.user,
        'other_field': 'new_value'
    }
    response = self.client.post(url, data)

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Profile.objects.count(), 2)
