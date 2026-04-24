from SystemForTezer.SystemsPay.ReplenishExchangeSystem.ExchangeCurrencyTezer.ECTZ import AuthSystemExchangePay

ectz = AuthSystemExchangePay("/SystemForTezer/SystemsPay/ExchangeCurrencyTezer\\tokens\id_for_keys.json")
print(ectz.OAuth_Update("C:\PyProg\ETCSto_Tezer\SystemForTezer\ExchangeCurrencyTezer\\tokens\get_post_token.json"))