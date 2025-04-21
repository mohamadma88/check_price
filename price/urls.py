from django.urls import path
from .views import PriceView

app_name = 'price'
urlpatterns = [
    path('price', PriceView.as_view(), name='price')
]
