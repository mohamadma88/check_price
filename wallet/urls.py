from django.urls import path
from .views import wallet , CurrencyView , WalletUserView , CryptoWalletView , TransactionView
from rest_framework.routers import DefaultRouter

app_name = 'wallet'
urlpatterns = [
    path('wallet',wallet,name='wallet'),
]

router = DefaultRouter()
router.register(r'currency', CurrencyView, basename='currency')
router.register(r'walletuser', WalletUserView, basename='walletuser')
router.register(r'cryptowallet', CryptoWalletView, basename='crypto_wallet')
router.register(r'transaction', TransactionView, basename='transaction')
urlpatterns += router.urls
