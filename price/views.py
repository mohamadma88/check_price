from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework import status
from .symbols import valid_symbol
from tabdeal.spot import Spot


class PriceView(APIView):
    def get(self, request):
        symbol = request.query_params.get('symbol')
        if not symbol:
            return Response({'error': 'Symbol is required'}, status=status.HTTP_400_BAD_REQUEST)
        symbol = symbol.upper()
        if symbol not in valid_symbol:
            return Response({'error': 'symbol is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # nobitex
            url = f'https://api.nobitex.ir/v3/orderbook/{symbol}'
            response = requests.get(url)
            data = response.json()
            # print(data)
            last_trade_nobitex = data['lastTradePrice']
            ask_nobitex = data['asks'][:4]
            bid_nobitex = data['bids'][:4]
        nobitex_fee_ask = [(float(ask[0]) * 1.03, ask[1]) for ask in ask_nobitex][:4]
        nobitex_fee_bid = [(float(bid[0]) * 1.03, bid[1]) for bid in bid_nobitex][:4]

        # tabdeal
        client = Spot()
        order_book = client.depth(
            symbol=f'{symbol}',
            limit=4
        )
        ask_tabdeal = order_book['asks'][:4]
        bid_tabdeal = order_book['bids'][:4]

        tabdeal_fee_ask = [(float(bid[0]) * 1.03, bid[1]) for bid in ask_tabdeal][:4]
        tabdeal_fee_bid = [(float(bid[0]) * 1.03, bid[1]) for bid in bid_tabdeal][:4]

        # wallex
        resp2 = requests.get(f'https://api.wallex.ir/v1/depth?symbol={symbol}')
        data2 = resp2.json()

        ask_wallex = data2['result']['ask'][:4]
        bid_wallex = data2['result']['bid'][:4]

        wallex_fees_ask = []
        wallex_fees_bid = []

        for ask in ask_wallex:
            wallex_fee_ask = float(ask['price']) * 1.03
            wallex_fees_ask.append({
                'original_price': float(ask['price']),
                'wallex_fee_ask': wallex_fee_ask
            })

        for bid in bid_wallex:
            wallex_fee_bid = float(bid['price']) * 1.03
            wallex_fees_bid.append({
                'original_price': float(bid['price']),
                'wallex_fee_bid': wallex_fee_bid
            })

            min_price_nobitex_fee_ask = min([price[0] for price in nobitex_fee_ask])
            min_price_tabdeal_fee_ask = min([price[0] for price in tabdeal_fee_ask])
            min_price_nobitex_fee_bid = min([price[0] for price in nobitex_fee_bid])
            min_price_tabdeal_fee_bid = min([price[0] for price in tabdeal_fee_bid])

            return Response({
                # nobitex
                'last trade nobitex': last_trade_nobitex, 'asks nobitex': ask_nobitex,
                'bids nobitex': bid_nobitex,
                'nobitex fee ask': nobitex_fee_ask,
                'nobitex fee bid': nobitex_fee_bid,
                # tabdeal
                'ask tabdeal': order_book['asks'],
                'bids tabdeal': order_book['bids'],
                'tabdeal fee ask': tabdeal_fee_ask,
                'tabdeal fee bid': tabdeal_fee_bid,
                # wallex
                'asks wallex': ask_wallex,
                'bids wallex': bid_wallex,
                'wallex fee ask': wallex_fees_ask,
                'wallex fee bid': wallex_fees_bid,
                # min price between exchanges
                'min_price_nobitex ask': min_price_nobitex_fee_ask,
                'min_price_tabdeal ask': min_price_tabdeal_fee_ask,
                'min_price_nobitex bid': min_price_nobitex_fee_bid,
                'min_price_tabdeal bid': min_price_tabdeal_fee_bid,

            }, status=status.HTTP_200_OK)
