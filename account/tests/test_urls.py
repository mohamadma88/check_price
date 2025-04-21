from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from account.views import OtpVerificationView, UserLoginView, ProfileView


class AccountUrlTest(APITestCase):
    def test_register_url(self):
        url = reverse('account:register')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_Otp_url(self):
        url = reverse('account:otp')
        self.assertEqual(resolve(url).func.view_class,OtpVerificationView)

    def test_Profile_url(self):
        url = reverse('account:profile')
        self.assertEqual(resolve(url).func.view_class,ProfileView)



