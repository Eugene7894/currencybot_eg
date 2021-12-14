import requests
import json

from config import keys

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Введена неправильная или несуществующая валюта - "{base}"')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Введена неправильная или несуществующая валюта - "{quote}"')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректно указано кол-во - "{amount}"')
        if base == quote:
            raise APIException('Нельзя конвертировать в ту же валюту')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        convert_res = json.loads(r.content)[keys[quote]] * amount
        return convert_res
