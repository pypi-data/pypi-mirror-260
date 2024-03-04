from binance import CryptoExchangeBinanceWS


class CryptoExchangeFactory:
    @staticmethod
    def create(exchange_id, market, symbol, callback, logger):
        if exchange_id.lower() == "binance":
            return CryptoExchangeBinanceWS(market, symbol, callback, logger)
        else:
            raise ValueError(f"Unsupported exchange: '{exchange_id}'")
