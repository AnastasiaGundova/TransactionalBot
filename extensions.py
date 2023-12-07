import requests
import json
from config import currencies


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str, language: str):
        if quote == base:
            raise APIException(f"Введены две одинаковые валюты {quote}" if language == "russian" else f"Two identical\
currencies have been found {quote}")
        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}" if language == "russian" else f"The currency \
could not be processed {quote}")
        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}" if language == "russian" else f"Failed to \
process the {base} currency")
        try:
            amount = float(amount)
        except KeyError:
            raise APIException(f"Не удалось обработать количество{amount}")
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[currencies[base]]
        return total_base
