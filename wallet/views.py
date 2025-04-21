from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import Wallet, Currency, CryptoWallet, WalletUser, Transaction
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from rest_framework.viewsets import ModelViewSet
from .serializers import CurrencySerializer, TransactionSerializer, CryptoWalletSerializer, \
    WalletUserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wallet(request):
    user = request.user
    amount_str = request.data.get('amount')

    if amount_str is None:
        return Response({"error": "amount must be specified"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = Decimal(amount_str)

        if amount <= 0:
            return Response({"error": "amount must be positive"}, status=status.HTTP_400_BAD_REQUEST)

        wallet, created = Wallet.objects.get_or_create(user=user)

        if wallet.amount is None:
            wallet.amount = 0

        wallet.amount += amount
        wallet.save()
        return Response({"balance": wallet.amount}, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"error": "amount must be a valid number"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrencyView(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class WalletUserView(ModelViewSet):
    queryset = WalletUser.objects.all()
    serializer_class = WalletUserSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)


class CryptoWalletView(ModelViewSet):
    serializer_class = CryptoWalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CryptoWallet.objects.filter(wallet__user=self.request.user)


class TransactionView(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()