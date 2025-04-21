from rest_framework.test import APITestCase
from account.models import User
from wallet.models import Wallet, Currency, CryptoWallet, Transaction, WalletUser
from django.utils.translation import gettext_lazy as _


class WalletModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(phone='11223344556', password='1234')
        cls.wallet = Wallet.objects.create(user=cls.user, amount='11.00')

    def test_amount_label(self):
        field_label = self.wallet._meta.get_field('amount').verbose_name
        self.assertEqual(field_label, _('amount'))

    def test_wallet_creation(self):
        wallet = Wallet.objects.create(user=self.user, amount=100.000)
        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.amount, 100.000)

    def test_wallet_user_str(self):
        self.assertEqual(str(self.wallet), '11223344556-11.00')


class CurrencyTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.currency = Currency.objects.create(name='btcusdt')

    def test_currency_name_uniqueness(self):
        Currency.objects.create(name='EUR')
        with self.assertRaises(Exception) as context:
            Currency.objects.create(name='btcusdt')

    def test_name_currency(self):
        field_label = self.currency._meta.get_field('name').verbose_name
        self.assertEqual(field_label, _('name'))


class CryptoWalletTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone='11223344556', password='1234')
        cls.wallet = WalletUser.objects.create(user=cls.user)
        cls.currency = Currency.objects.create(name='btcusdt')
        cls.cryptowallet = CryptoWallet.objects.create(wallet=cls.wallet, currency=cls.currency, balance=12.00)

    def test_cryptowallet_creation(self):
        self.assertIsInstance(self.cryptowallet, CryptoWallet)
        self.assertEqual(self.cryptowallet.wallet, self.wallet)
        self.assertEqual(self.cryptowallet.currency, self.currency)
        self.assertEqual(self.cryptowallet.balance, 12.00)

    def test_wallet_field_label(self):
        field_label = self.cryptowallet._meta.get_field('wallet').verbose_name
        self.assertEqual(field_label, _('wallet'))

    def test_currency_field_label(self):
        field_label = self.cryptowallet._meta.get_field('currency').verbose_name
        self.assertEqual(field_label, _('currency'))

    def test_balance_field_label(self):
        field_label = self.cryptowallet._meta.get_field('balance').verbose_name
        self.assertEqual(field_label, _('balance'))

class TransactionTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone='11223344556', password='1234')
        cls.walletuser = WalletUser.objects.create(user=cls.user)
        cls.currency = Currency.objects.create(name='btcusdt')
        cls.cryptowallet = CryptoWallet.objects.create(wallet=cls.walletuser, currency=cls.currency, balance=12.00)
        cls.transaction = Transaction.objects.create(wallet=cls.cryptowallet, amount=12.00,transaction='ok')

    def test_transaction_creation(self):
        self.assertIsInstance(self.transaction, Transaction)
        self.assertEqual(self.transaction.wallet, self.cryptowallet)
        self.assertEqual(self.transaction.amount, 12.00)
        self.assertEqual(self.transaction.transaction, 'ok')

    def test_wallet_field_label(self):
        field_label = self.transaction._meta.get_field('wallet').verbose_name
        self.assertEqual(field_label, _('wallet'))

    def test_amount_field_label(self):
        field_label = self.transaction._meta.get_field('amount').verbose_name
        self.assertEqual(field_label, _('amount'))

    def test_transaction_field_label(self):
        field_label = self.transaction._meta.get_field('transaction').verbose_name
        self.assertEqual(field_label, _('transaction'))

