from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from wallet.views import wallet


class WalletUrlsTest(APITestCase):
    def test_wallet_url(self):
        url = reverse('wallet:wallet')
        self.assertEqual(resolve(url).func, wallet)
