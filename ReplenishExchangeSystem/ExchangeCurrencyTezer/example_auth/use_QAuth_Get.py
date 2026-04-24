from SystemForTezer.SystemsPay.ReplenishExchangeSystem.ExchangeCurrencyTezer.ECTZ import AuthSystemExchangePay

ectz = AuthSystemExchangePay("/SystemForTezer/SystemsPay/ExchangeCurrencyTezer\\tokens\id_for_get.json")

#создаст json file с токеном рядом с файлом ECTZ.py
print(ectz.OAuth_Get()) #в начале обновите код по адресу https://www.donationalerts.com/oauth/authorize?client_id=abc123&redirect_uri=http://localhost:8000/callback&response_type=code&scope=oauth-donation-index+oauth-user-show