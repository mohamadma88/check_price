from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from price.views import PriceView


class PriceUrlTest(APITestCase):
    def test_price_url(self):
        url = reverse('price:price')
        self.assertEqual(resolve(url).func.view_class, PriceView)

