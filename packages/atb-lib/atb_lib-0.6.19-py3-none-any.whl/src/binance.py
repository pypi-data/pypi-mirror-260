import json

from helpers import find_current_avg_price
from exchange_ws import CryptoExchangeWS


class CryptoExchangeBinanceWS(CryptoExchangeWS):
    # noinspection SpellCheckingInspection
    symbols = {"BTC/USDT": "btcusdt", "ETH/USDT": "ethusdt"}
    exchange = 'binance'

    def __init__(self, market, symbol, callback, logger):
        self._market = market.lower()
        self._symbol = symbol
        self._logger = logger
        localised_symbol = self.symbols.get(symbol)

        if not localised_symbol:
            raise ValueError(f"Unsupported symbol: '{symbol}'")

        if self._market == 'spot':
            url = f"wss://stream.binance.com:9443/ws/{localised_symbol}@depth"
        elif self._market == 'futures':
            url = f"wss://fstream.binance.com/ws/{localised_symbol}@depth"
        else:
            raise ValueError(f"Incorrect market: '{market}'")

        super().__init__(url, callback, logger)

    def _parse_message(self, message):
        try:
            result = None
            data = json.loads(message)

            if data['e'] == 'depthUpdate':
                cid = data.get('u', 0)
                pid = data.get('pu', 0) if self._market == 'futures' else data.get('U', 0) - 1
                ap = find_current_avg_price(data['b'], data['a'])
                result = {
                    'X': self.exchange,
                    'M': self._market,
                    'S': self._symbol,
                    'E': data['E'],
                    'CID': cid,
                    'PID': pid,
                    'AP': ap,
                    'A': data['a'],
                    'B': data['b']
                }

            return result
        except json.JSONDecodeError:
            self._logger.error("Error parsing JSON message")
