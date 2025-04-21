from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from account.models import User
from django.urls import reverse
from decimal import Decimal
from wallet.models import Wallet


class WalletTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone='11223344556', password='1234')
        cls.client = APIClient()

    def test_wallet_creation_with_valid_amount(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('wallet:wallet')
        data = {
            'amount': '50.00'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], Decimal('50.00'))
        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(wallet.amount, Decimal('50.00'))

    def test_wallet_creation_with_negative_amount(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('wallet:wallet')
        data = {
            'amount': '-10.00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "amount must be positive")

    def test_wallet_creation_without_amount(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('wallet:wallet')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "amount must be specified")
