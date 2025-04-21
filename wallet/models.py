from django.db import models
from account.models import User


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, verbose_name='amount')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.amount}'


class Currency(models.Model):
    name = models.CharField(max_length=50 , unique=True,verbose_name='name')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WalletUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.phone


class CryptoWallet(models.Model):
    wallet = models.ForeignKey(WalletUser, on_delete=models.CASCADE,verbose_name='wallet')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,verbose_name='currency')
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0.00,verbose_name='balance')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wallet', 'currency')

    def __str__(self):
        return f'{self.wallet}-{self.balance}'


class Transaction(models.Model):
    wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE,verbose_name='wallet')
    amount = models.DecimalField(max_digits=20, decimal_places=8,verbose_name='amount')
    transaction = models.CharField(max_length=10,verbose_name='transaction')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.wallet}-{self.amount}-{self.transaction}'
