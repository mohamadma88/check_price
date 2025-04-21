from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class PriceViewTest(APITestCase):
    def test_price_view(self):
        url = reverse('price:price')
        response = self.client.get(url, {'symbol': 'BTCUSDt'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_price_view_missing_symbol(self):
        url = reverse('price:price')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Symbol is required')

    def test_price_view_invalid_symbol(self):
        url = reverse('price:price')
        response = self.client.get(url, {'symbol': 'INVALID_SYMBOL'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'symbol is not valid')
