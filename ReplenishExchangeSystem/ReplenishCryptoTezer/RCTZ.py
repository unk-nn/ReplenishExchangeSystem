import requests as rqs
import asyncio
import aiohttp

class TezerReplenish():
    def __init__(self, atoken:str):
        self.__atoken = atoken #API_TOKEN
        self.__base_url = "https://testnet-pay.crypt.bot/api/" #https://pay.crypt.bot/api/
        self.__bheaders = {"Crypto-Pay-API-Token":self.__atoken, "Content-Type": "application/json"} #base_headers

    def get_balance(self):
        responce = rqs.get(
            self.__base_url+"getBalance",
            headers=self.__bheaders
        )
        return responce.json()
    def get_invoice(self, invoice_id:int, all:bool=False):
        if all == True:
            responce = rqs.get(
                self.__base_url + 'getInvoices',
                headers=self.__bheaders
            )

            return responce.json()
        else:
            responce = rqs.get(
                self.__base_url+'getInvoices',
                headers=self.__bheaders,
                params={'invoice_ids':str(invoice_id)}
            )
            return responce.json()

    async def check_invoice(self, invoice_id:int):
        while True:
            await asyncio.sleep(15.0)

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.__base_url+'getInvoices',
                    headers=self.__bheaders,
                    params={'invoice_ids': str(invoice_id)}) as data: responce = await data.json()

            if responce['result']['items'] == []:
                return False  # возможно заменить на код локальной ошибки
            else:
                if int(responce['result']['items'][0]['invoice_id']) == invoice_id:
                    status = responce['result']['items'][0]['status']

                    if status == 'paid':
                        return True
                    elif status == 'expired':
                        return False # возможно заменить на код локальной ошибки
                else:
                    return False #возможно заменить на код локальной ошибки

    async def open_invoice(self, amount:float=6, asset:str="USDT", description:str="Replenishment of Teezer wallet for 6 USDT", expire_time:int=900):
        prm = {
            "amount": amount,  # Сумма счета
            "asset": asset,  # Валюта (например, USDT, TON)
            "description": description,  # Описание
            "expires_in": expire_time,  # Время истечения (в секундах, например 15 минут)
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.__base_url + "createInvoice",
                headers=self.__bheaders,
                params=prm) as data: return await data.json()
    async def close_invoice(self, invoice_id:int):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.__base_url + "deleteInvoice",
                headers=self.__bheaders,
                params={"invoice_id": invoice_id}) as data: return await data.json()