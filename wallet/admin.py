from django.contrib import admin
from .models import Wallet, Currency, CryptoWallet, WalletUser, Transaction

admin.site.register(Wallet)
admin.site.register(Currency)
admin.site.register(CryptoWallet)
admin.site.register(WalletUser)
admin.site.register(Transaction)

