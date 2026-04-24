import requests
import json
from SystemForTezer.SystemsPay.ReplenishExchangeSystem.ExchangeCurrencyTezer.DataBase import AuthTransaction_db as ata
import asyncio
import aiohttp

class AuthSystemExchangePay():
    def __init__(self, json_file:str):
        self.__jft = json_file

    def OAuth_Get(self):
        with open(self.__jft, mode='r', encoding='UTF-8') as jf:
            json_post = json.load(jf)

        data = {
            'grant_type': "authorization_code", #authorization_code
            'client_id': json_post["client_id"], #YOUR_CLIENT_ID
            'client_secret': json_post["client_secret"], #YOUR_CLIENT_SECRET #KEY
            'redirect_uri': json_post["redirect_uri"], #YOUR_REDIRECT_URI #http://localhost:8000/callback
            'code': json_post["code"] #AUTHORIZATION_CODE #from https://www.donationalerts.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8000/callback&response_type=code&scope=oauth-donation-index+oauth-user-show
        }
        response = requests.post("https://www.donationalerts.com/oauth/token", data=data)

        if response.status_code == 200:
            with open('get_post_token.json', 'w', encoding='UTF-8') as gpt:
                gpt.write(str(response.json()).replace("'", '"'))
            return response.json()
        else:
            return {"FalledStatus":response.status_code, "Error":response.json()}
    def OAuth_Update(self, json_file_rtoken:str):
        with open(json_file_rtoken, mode='r', encoding='UTF-8') as jfr:
            refresh_token = json.load(jfr)["refresh_token"]
        with open(self.__jft, mode='r', encoding='UTF-8') as jfc:
            clients = json.load(jfc)

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": clients["client_id"],
            "client_secret": clients["client_secret"]
        }
        response = requests.post("https://www.donationalerts.com/oauth/token", data=data)

        if response.status_code == 200:
            with open('update_post_token.json', 'w', encoding='UTF-8') as upt:
                upt.write(str(response.json()).replace("'", '"'))
            return response.json()
        else:
            return {"FalledStatus": response.status_code, "Error": response.json()}

class SystemExchangePay():
    def __init__(self, token:str):
        self.__tapi = token
        self.__list_task = {}

    def get_paymenets(self):
        resdata = requests.get(
            'https://www.donationalerts.com/api/v1/alerts/donations',

            headers={
                'Authorization':f'Bearer {self.__tapi}'
            }
        )

        if resdata.status_code == 200:
            return resdata.json()
        else:
            return {'FalledStatus':resdata.status_code, 'Error':resdata.json()}
    async def OneCheck_paymenets(self, address_wallet:str, amount:float, currency:str):
        legit = ata.AuthTransactionAllerts()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://www.donationalerts.com/api/v1/alerts/donations',
                    headers={
                        'Authorization': f'Bearer {self.__tapi}'
                    }
            ) as data: resdata = await data.json()

        if data.status == 200:
            for i in resdata['data']:
                if str(i['message']) == str(address_wallet):
                    if str(i['currency']) == str(currency):
                        if float(i['amount']) == float(amount):
                            pay = True

                            for row in legit.select():
                                if str(row.transaction) == str(i['id']):
                                    pay = False
                            if pay == True:
                                legit.create(transaction=str(i['id']), address=address_wallet, amount=str(amount), currency=currency)
                                return True
            return False
        else:
            return {'FalledStatus': data.status, 'Error': await data.json()}

    async def __timeout_invoice(self):
        await asyncio.sleep(900)
    async def __open_invoice_script(self, user_id:int, address_wallet:str, amount:float, currency:str):
        try:
            stop = asyncio.create_task(self.__timeout_invoice())

            while True:
                if stop.done():
                    del self.__list_task[user_id]
                    return False
                else:
                    await asyncio.sleep(15.0)
                    status = await self.OneCheck_paymenets(address_wallet, amount, currency)

                    if status == True:
                        del self.__list_task[user_id]
                        return True
        except asyncio.CancelledError:
            return False

    async def open_invoice_allerts(self, user_id:int, address_wallet:str, amount:float, currency:str):
        task = asyncio.create_task(self.__open_invoice_script(user_id, address_wallet, amount, currency))
        self.__list_task[user_id] = task

        return task
    async def close_invoice_allerts(self, user_id:int):
        task = self.__list_task.get(user_id)

        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.__list_task[user_id]