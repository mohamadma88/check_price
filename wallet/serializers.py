from rest_framework import serializers
from .models import Wallet, CryptoWallet, WalletUser, Currency, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'amount']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name']


class WalletUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletUser
        fields = ['id', 'user']


class CryptoWalletSerializer(serializers.Serializer):
    class Meta:
        model = CryptoWallet
        fields = ['id', 'wallet', 'currency', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'amount', 'transaction']
