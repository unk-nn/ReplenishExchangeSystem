# ReplenishExchangeSystem
Здесь вы найдете информацию о системе RES и ее внедрении 

---

# Содержание
- [1. ReplenishExchangeSystem – Общее описание](#1-replenishexchangesystem--общее-описание)
  - [1.1 Файл api_tokens.json](#11-файл-api_tokensjson)
  - [1.2 Модуль GetPathToken.py](#12-модуль-getpathtokenpy)
- [2. Модуль ReplenishCryptoTezer (RCTZ)](#2-модуль-replenishcryptotezer-rctz)
  - [2.1 Файлы модуля RCTZ](#21-файлы-модуля-rctz)
  - [2.2 Класс TezerReplenish](#22-класс-tezerreplenish)
    - [2.2.1 Инициализация класса](#221-инициализация-класса)
    - [2.2.2 Методы класса](#222-методы-класса)
      - [get_balance – Получение баланса](#get_balance--получение-баланса)
      - [get_invoice – Получение счёта](#get_invoice---получение-счета)
      - [check_invoice – Проверка статуса счёта](#check_invoice--проверка-оплаты-счёта)
      - [open_invoice – Создание нового счёта](#open_invoice--создание-инвойса)
      - [close_invoice – Закрытие счёта](#close_invoice--закрытие-инвойса)
  - [2.3 Пример использования с aiogram](#23-пример-использования-с-aiogram)
    - [2.3.1 Основные функции main.py](#231-основные-функции-mainpy)
- [3. Модуль ExchangeCurrencyTezer (ECTZ)](#3-модуль-exchangecurrencytezer-ectz)
  - [3.1 DataBase](#31-database)  
      - [3.1.1 AuthTransaction.db](#311-authtransactiondb)  
      - [3.1.2 AuthTransaction_db.py](#312-authtransaction_dbpy)  
  - [3.2 Tokens](#32-tokens)  
      - [get_post_token.json](#get_post_tokenjson)  
      - [id_for_keys.json](#id_for_keysjson)  
      - [update_post_token.json](#update_post_tokenjson)  
  - [3.3 Documentions](#33-documentions)  
      - [3.3.1 Example_files](#331-example_files)  
  - [3.4 Класс AuthSystemExchangePay](#34-класс-authsystemexchangepay)  
      - [3.4.1 Инициализация класса](#341-инициализация-класса)  
      - [3.4.2 Методы класса](#342-методы-класса)  
  - [3.5 Класс SystemExchangePay](#35-класс-systemexchangepay)  
      - [3.5.1 Инициализация класса](#351-инициализация-класса)  
      - [3.5.2 Методы класса](#352-методы-класса)  
  - [3.6 Пример использования с aiogram](#36-пример-использования-с-aiogram)  
      - [3.6.1 Функции main.py](#361-функции-mainpy)

---

# 1. ReplenishExchangeSystem
ReplenishExchangeSystem включает две независимые системы оплаты: криптовалютой и фиатными валютами (рублями, долларами и др.).  
Этот репозиторий предназначен для изучения работы обеих систем и их корректной интеграции в общую инфраструктуру проекта.  
Цель — получить глубокое понимание механизмов взаимодействия с платежными API и обеспечить стабильную, надёжную и безопасную работу платежных процессов.

## 1.1 Файл `api_tokens.json`
Файл `api_tokens.json` используется для хранения токенов доступа к API.  
Он необходим для работы модулей, взаимодействующих с API.  
Добавлен в репозиторий для понимания структуры файла и не более.

## 1.2 Модуль `GetPathToken.py`
Файл `GetPathToken.py` содержит вспомогательные функции для работы с путями к файлам и извлечения токенов из JSON-файлов. Он используется в проекте ReplenishExchangeSystem для упрощения доступа к конфигурационным данным.

### Основные функции файла
Файл включает две ключевые функции: `get_path` и `get_json_token`. Эти функции обеспечивают удобное получение путей к файлам и извлечение токенов из JSON-файлов, что делает проект более модульным и переносимым.

#### 1. Функция `get_path`

**Описание функции:**  
Функция `get_path` формирует абсолютный путь к указанному файлу относительно директории, в которой находится скрипт. Это полезно для доступа к файлам конфигурации, таким как `api_tokens.json`, независимо от текущей рабочей директории.

> **Важно:** Для корректной работы функция должна вызываться из скрипта, расположенного в главной папке проекта, так как путь формируется относительно местоположения вызывающего файла.

**Код функции:**
```python
from pathlib import Path

def get_path(folders: list, file: str):
    main_dir = Path(__file__).parent
    return main_dir.joinpath(*folders, file)
```

**Параметры:**
- `folders` *(list)*: Список папок, составляющих путь к файлу относительно главной директории проекта.
- `file` *(str)*: Имя файла, к которому нужно сформировать путь.

**Возвращает:**
- `Path`: Объект `pathlib.Path`, представляющий абсолютный путь к файлу.

**Пример использования:**
```python
from GetPathToken import get_path

# Формирование пути к файлу api_tokens.json
path = get_path(["SystemForTezer"], "api_tokens.json")
print(path)  # Например: C:\PyProg\ETCSto_Tezer\SystemForTezer\api_tokens.json
```

**Что демонстрирует пример:**  
Пример показывает, как использовать функцию `get_path` для получения пути к файлу `api_tokens.json`, расположенному внутри проекта в папке `SystemForTezer`.

#### 2. Функция `get_json_token`

**Описание функции:**  
Функция `get_json_token` извлекает значение токена из JSON-файла по указанному ключу. Она используется для получения API-токенов.

**Код функции:**
```python
import json

def get_json_token(json_file: str, type_token: str = 'access_token'):
    with open(json_file, mode='r', encoding='UTF-8') as get_token:
        json_post = json.load(get_token)
        return json_post[type_token]
```

**Параметры:**
- `json_file` *(str)*: Путь к JSON-файлу, содержащему токены (например, `api_tokens.json`).
- `type_token` *(str, опционально)*: Ключ, по которому извлекается токен из JSON. По умолчанию — `"access_token"`.

**Возвращает:**
- `str`: Значение токена, соответствующее указанному ключу.

**Пример использования:**
```python
from GetPathToken import get_json_token

# Извлечение токена для Telegram-бота
token = get_json_token('C:\\PyProg\\ETCSto_Tezer\\SystemForTezer\\api_tokens.json', type_token="tzr_test_bot_api")
print(token)  # Например: "123456:ABCDEF..."

# Извлечение токена для CryptoBot API, также пример применения двух функций одновременно
crypto_token = get_json_token(get_path(["SystemForTezer"], "api_tokens.json"), type_token="test_crypto_api")
print(crypto_token)  # Например: "abcdef123456..."
```

**Что демонстрирует пример:**  
Пример показывает, как извлечь токены для Telegram-бота и CryptoBot API из файла `api_tokens.json` с использованием функции `get_json_token` и функции `get_path`.

> **Модульность**: Функции `get_path` и `get_json_token` делают код более переносимым, позволяя централизованно управлять доступом к конфигурационным файлам.

> **Важно**: В примерах используются пути к файлу `api_tokens.json`, соответствующие тестовой среде. Для продакшн-версии убедитесь, что пути и токены обновлены.

### Использование в проекте
- В `RCTZ/main.py`:
  ```python
  bot = Bot(get_json_token(get_path(['SystemForTezer'], 'api_tokens.json'), type_token="tzr_test_bot_api"))
  dp = Dispatcher(storage=MemoryStorage())
  rctz = TezerReplenish(get_json_token(get_path(['SystemForTezer'], 'api_tokens.json'), type_token="test_crypto_api"))
  ```

- Это позволяет инициализировать Telegram-бот и модуль `RCTZ` с использованием токенов из `api_tokens.json`.

> **Вывод:** Файл `GetPathToken.py` предоставляет утилиты для работы с путями и токенами, упрощая конфигурацию проекта. Функция `get_path` обеспечивает формирование путей к файлам, а `get_json_token` позволяет безопасно извлекать API-токены. Эти функции делают проект более структурированным и удобным для поддержки, особенно при работе с конфигурационными файлами.

---

# 2. Модуль ReplenishCryptoTezer (RCTZ)
Модуль ReplenishCryptoTezer (RCTZ) предназначен для интеграции с CryptoBot API и управления криптовалютными платежами на платформе Tezer.  
Основой модуля является класс TezerReplenish, который предоставляет набор методов для выполнения ключевых операций:
- получение баланса кошелька,
- создание новых платежных счетов (инвойсов),
- проверка статуса оплаты счетов,
- закрытие счетов по необходимости,
- получение информации о конкретных или всех счетах.
  
Модуль сочетает синхронные запросы с использованием библиотеки requests и асинхронные вызовы через aiohttp и asyncio, что позволяет удобно внедрять его в асинхронные приложения, включая Telegram-боты на базе aiogram.
В рамках проекта ReplenishExchangeSystem этот модуль служит ключевым компонентом для реализации стабильного и безопасного процесса пополнения криптовалютой баланса пользователей.

## 2.1 Файлы модуля RCTZ
Модуль `ReplenishCryptoTezer (RCTZ)` состоит из ключевых файлов, обеспечивающих его функциональность и интеграцию:
- **`RCTZ.py`** — основной файл, содержащий класс `TezerReplenish`.  
  Этот класс реализует взаимодействие с CryptoBot API, включая создание, проверку и закрытие счетов, а также получение баланса.  
  О классе и его методах можно узнать ниже.
- **`main.py`** — пример использования модуля с Telegram-ботом на базе `aiogram`.  
  Демонстрирует процесс создания счетов, обработку пользовательских запросов, отслеживание статуса оплаты и отмену платежей.
- **`api_tokens.json`** — конфигурационный файл, содержащий необходимые токены доступа к API.  
  Сам файл **отсутствует в папке модуля**, но используется во всём проекте для безопасного хранения ключей и упрощения конфигурации.

Данная структура обеспечивает удобство поддержки и расширения функционала модуля.

## 2.2 Класс `TezerReplenish`
Класс `TezerReplenish` — это основной инструмент модуля `RCTZ` для работы с **CryptoBot API**, обеспечивающий управление криптовалютными платежами в системе Tezer.  
Его задачи:  
- взаимодействие с API для получения информации о балансе и счетах,  
- создание новых платежных счетов,  
- отслеживание их статуса в асинхронном режиме,  
- закрытие счетов при необходимости.  

Класс объединяет **синхронные** (на основе библиотеки `requests`) и **асинхронные** (на основе `aiohttp` и `asyncio`) методы, что позволяет гибко интегрировать его в проекты разного уровня сложности — от простых скриптов до асинхронных приложений и ботов.  
О структуре и назначении каждого метода можно узнать ниже в подпунктах 2.2.

## 2.2.1 Инициализация класса
Класс `TezerReplenish` инициализируется с использованием API-токена, необходимого для авторизации запросов в CryptoBot API.

### Пример инициализации:
```python
from RCTZ import TezerReplenish
from SystemForTezer.SystemsPay.ReplenishExchangeSystem.ExchangeCurrencyTezer.ECTZ import get_json_token

# Получаем API-токен из внешнего файла конфигурации
token = get_json_token(
    r'C:\PyProg\ETCSto_Tezer\SystemForTezer\api_tokens.json',  # Путь к конфигурационному файлу
    type_token="test_crypto_api"  # Ключ, по которому извлекается нужный токен
)

# Создаём экземпляр класса с этим токеном
rctz = TezerReplenish(token)
```

### Что здесь происходит:
- Функция `get_json_token` загружает файл `api_tokens.json` и извлекает из него токен по указанному ключу (`type_token`).
- `token` — строка с самим API-токеном.
- Экземпляр `rctz` создаётся с этим токеном, что позволяет выполнять авторизованные запросы к CryptoBot API.
  
### При создании экземпляра:
- `atoken` — строка с токеном доступа.
- Устанавливается базовый URL для API (`https://testnet-pay.crypt.bot/api/` по умолчанию, в продакшн-версии заменяется на боевой).
- Формируются заголовки (`headers`) с токеном и типом содержимого (`application/json`).

> **Важно:** Для работы в тестовой среде используется [testnet-URL](https://prostocoin.io/blog/testnet?). Перед внедрением в боевой режим необходимо заменить его на  
> `https://pay.crypt.bot/api/` в файле `RCTZ.py`.

---

## 2.2.2 Методы класса
Здесь вы можете ознакомиться с методами класса `TezerReplenish` и найти документацию по их использованию.

## get_balance — получение баланса
### `get_balance()`

**Описание метода:**  
Метод `get_balance` используется для получения текущего баланса всех доступных валют на счёте в CryptoBot API. Это синхронный метод, который возвращает информацию обо всех активах кошелька: доступный остаток, замороженные суммы и их значения в долларах США. Этот метод особенно полезен для мониторинга состояния средств, доступных для проведения операций.

> **Важно:** Этот метод не используется непосредственно в проекте, но он может понадобиться в будущем, если функционал модуля будет расширяться.

> **Важно:** Этот метод выводит исключительно информацию о средствах на кошельке аккаунта, на котором был создан `API`. То есть показывает средства, выведенные из "`API`-приложения". Если кошелёк и аккаунт используются не только для приложения или для нескольких приложений, то на балансе кошелька невозможно отследить баланс конкретного приложения. Чтобы посмотреть баланс конкретного приложения или вывести средства приложения на кошелёк, зайдите во вкладку в боте `CryptoBot`: `main/CryptoPay/Мои приложения/NAME_YOUR_APP`.  

**Аргументы:**
- Аргументы отсутствуют. Метод возвращает баланс всех доступных валют.

**Пример использования:**
```python
# Получение баланса кошелька
balance = rctz.get_balance()
print(balance)
```

**Что демонстрирует пример:**  
Пример показывает, как вызвать метод `get_balance` для получения полного списка активов на счету, включая их количество и пересчитанную стоимость в долларах США.

**Возвращает:**
- `dict` — JSON-объект с информацией о балансе всех доступных валют.

**Пример возвращаемого JSON:**
```json
{
  "ok": true,
  "result": [
    {
      "currency_type": "crypto",
      "asset": "TRX",
      "available": "100.5",
      "onhold": "0",
      "total_in_usd": "32.58"
    },
    {
      "currency_type": "crypto",
      "asset": "TON",
      "available": "50",
      "onhold": "0",
      "total_in_usd": "123.45"
    }
  ]
}
```
**Ключевые поля ответа:**
- `asset` — код валюты (например, `TRX`, `TON`).
- `available` — доступный баланс.
- `onhold` — средства, находящиеся в ожидании (замороженные).
- `total_in_usd` — пересчитанная стоимость актива в долларах США.

**Пример обработки JSON-ответа:**
```python
balance = rctz.get_balance()
if invoice['ok'] == 'true':
    for item in balance["result"]:
        print(f"Валюта: {item['asset']}, доступно: {item['available']}, заморожено: {item['onhold']}, в USD: {item['total_in_usd']}")
else:
    print("Ошибка получения баланса")
```
**Что демонстрирует пример:**  
Пример показывает, как обработать JSON-ответ метода `get_balance`: извлечь данные о каждой валюте и вывести доступный и замороженный баланс, а также стоимость актива в долларах США.

## get_invoice - получение счета
### `get_invoice(invoice_id: int, all: bool = False)`

**Описание метода:**  
Метод `get_invoice` позволяет получить информацию о конкретном счёте по его идентификатору или запросить список всех созданных счетов. Это синхронный метод, который напрямую обращается к API и возвращает ответ в формате JSON. Он используется для извлечения детальной информации о платёжных инвойсах: их статус, сумму, валюту, дату создания и другую связанную информацию.
> **Важно:** Этот метод не используется непосредственно в проекте, но он важен для понимания фундамента работы метода `check_invoice`, а также может применяться для целей анализа или парсинга информации об инвойсах.

**Аргументы:**
- `invoice_id` *(int)* — идентификатор счёта. Используется, если нужно получить данные конкретного инвойса.
- `all` *(bool, опционально)* — если `True`, метод возвращает информацию обо всех инвойсах, созданных через API. Если `False`, возращает только информацию о счете чей `invoice_id` был передан. `all` по умолчанию `False`. 

**Пример использования:**
```python
# Получение информации по конкретному счёту
invoice = rctz.get_invoice(invoice_id=123456)
print(invoice)

# Получение информации по всем счетам
all_invoices = rctz.get_invoice(invoice_id=0, all=True)
print(all_invoices)
```

**Что демонстрирует пример:**  
Пример показывает, как вызвать метод для получения информации как по одному конкретному счёту, так и по всем счетам. 

**Возвращает:**
- `dict` — JSON-объект с информацией о счёте или списке счетов. В случае успеха поле `ok` будет равно `True`, а в `result` будет содержаться информация об инвойсах.

**Пример возвращаемого JSON:**
```json
{
  "ok": true,
  "result": {
    "items": [
      {
        "invoice_id": 711707,
        "hash": "IVnjS1Gzph6Z",
        "currency_type": "crypto",
        "asset": "TRX",
        "amount": "3",
        "paid_asset": "TRX",
        "paid_amount": "3",
        "fee_asset": "TRX",
        "fee_amount": "0.09",
        "fee_in_usd": "0.02928742",
        "pay_url": "https://t.me/CryptoTestnetBot?start=IVnjS1Gzph6Z",
        "bot_invoice_url": "https://t.me/CryptoTestnetBot?start=IVnjS1Gzph6Z",
        "mini_app_invoice_url": "https://t.me/CryptoTestnetBot/app?startapp=invoice-IVnjS1Gzph6Z&mode=compact",
        "web_app_invoice_url": "https://testnet-app.send.tg/invoices/IVnjS1Gzph6Z",
        "description": "Replenishment of Tezer wallet for 3 TRX",
        "status": "paid",
        "created_at": "2025-08-01T07:00:30.465Z",
        "allow_comments": true,
        "allow_anonymous": true,
        "expiration_date": "2025-08-01T07:15:30.462Z",
        "paid_usd_rate": "0.32541579",
        "paid_at": "2025-08-01T07:00:44.495Z",
        "paid_anonymously": false
      }
    ]
  }
}
```
**Ключевые поля ответа:**
- `invoice_id` — уникальный идентификатор инвойса.
- `status` — статус счёта (`active`, `paid`, `expired`).
- `asset` — валюта платежа (например, `TRX`).
- `amount` — сумма платежа.
- `pay_url` / `mini_app_invoice_url` — ссылки для оплаты.
- `created_at` / `expiration_date` — даты создания и истечения действия счёта.
- `paid_amount`, `paid_at` — информация об оплате.
  
**Пример обработки JSON-ответа:**
```python
invoice = rctz.get_invoice(invoice_id=711707)
if invoice['ok'] == 'true':
    items = invoice["result"]["items"]
    for item in items:
        print(f"Счёт {item['invoice_id']} имеет статус: {item['status']} и сумму: {item['amount']} {item['asset']}")
else:
    print("Ошибка получения информации о счёте")
```
**Что демонстрирует пример:**  
Этот пример показывает, как обработать JSON-ответ метода: извлечь список инвойсов и вывести ключевую информацию о каждом (идентификатор, статус, сумму и валюту).

## check_invoice — проверка оплаты счёта
### `async check_invoice(invoice_id: int) -> bool`

**Описание метода:**  
Метод `check_invoice` предназначен для асинхронной проверки статуса определённого инвойса (счёта) по его `invoice_id`. Метод работает в цикле с задержкой 15 секунд и обращается к API `getInvoices`, чтобы отслеживать изменения статуса конкретного счёта. Он возвращает `True`, если счёт был оплачен, и `False`, если он истёк, не найден.

**Аргументы:**
- `invoice_id` *(int)* — уникальный идентификатор счёта, статус которого нужно отслеживать.

**Пример использования:**
```python
# Пример асинхронного вызова метода check_invoice
import asyncio

async def main():
    invoice_id = 711707
    result = await rctz.check_invoice(invoice_id)
    if result:
        print("Счёт был успешно оплачен!")
    else:
        print("Счёт не был оплачен или истёк.")

asyncio.run(main())
```

**Что демонстрирует пример:**  
Пример демонстрирует, как можно вызвать метод `check_invoice` в асинхронной функции, ожидая подтверждения успешной оплаты счёта. Это основа для обработки бизнес-логики, связанной с поступлением средств.

**Возвращает:**
- `True`, если инвойс успешно оплачен (`status == 'paid'`).
- `False`, если инвойс истёк (`status == 'expired'`), не существует или не соответствует `invoice_id`.

## open_invoice — создание инвойса
### `open_invoice(amount: int, asset: str = "USDT", description: str = "")`

**Описание метода:**  
Метод `open_invoice` используется для создания нового платёжного инвойса (счёта) с заданной суммой, валютой и описанием. Он асинхронно отправляет POST-запрос к API и возвращает JSON-объект с данными о только что созданном инвойсе. Этот метод является основой для начала платёжной сессии в системе.

**Аргументы:**
- `amount` *(int)* — сумма инвойса. Должна быть больше 0 и соответствовать минимальным требованиям по выбранному активу.
- `asset` *(str, опционально)* — тип валюты, в которой выставляется счёт. По умолчанию — "USDT". Можно использовать: `BTC`, `TON`, `ETH`, `TRX`, и т.д.
- `description` *(str, опционально)* — описание назначения платежа. Может отображаться пользователю при оплате.

**Пример использования:**
```python
invoice = await rctz.open_invoice(amount=3, asset="TRX", description="Replenishment of Tezer wallet for 3 TRX")
print(invoice)
```

**Что демонстрирует пример:**  
Этот пример показывает, как создать новый платёжный инвойс на сумму 3 TRX с описанием "Replenishment of Tezer wallet for 3 TRX". Метод возвращает JSON с данными для оплаты, включая URL-ссылки для разных интерфейсов Telegram.

**Возвращает:**
- `dict` — JSON-объект с данными созданного счёта. В случае успеха поле `ok` будет равно `True`, а в `result` содержаться данные нового инвойса.

**Пример возвращаемого JSON:**
```json
{
  "ok": true,
  "result": {
    "invoice_id": 715877,
    "hash": "IVwOgXfCUTnR",
    "currency_type": "crypto",
    "asset": "TRX",
    "amount": "3",
    "pay_url": "https://t.me/CryptoTestnetBot?start=IVwOgXfCUTnR",
    "bot_invoice_url": "https://t.me/CryptoTestnetBot?start=IVwOgXfCUTnR",
    "mini_app_invoice_url": "https://t.me/CryptoTestnetBot/app?startapp=invoice-IVwOgXfCUTnR&mode=compact",
    "web_app_invoice_url": "https://testnet-app.send.tg/invoices/IVwOgXfCUTnR",
    "description": "Replenishment of Tezer wallet for 3 TRX",
    "status": "active",
    "created_at": "2025-08-07T08:48:56.885Z",
    "allow_comments": true,
    "allow_anonymous": true,
    "expiration_date": "2025-08-07T09:03:56.883Z"
  }
}
```

**Ключевые поля ответа:**
- `invoice_id` — уникальный идентификатор нового счёта.
- `asset` — валюта, в которой выставлен счёт.
- `amount` — сумма инвойса.
- `status` — статус счёта (`active` — ожидает оплаты).
- `description` — описание платежа.
- `pay_url`, `bot_invoice_url`, `mini_app_invoice_url`, `web_app_invoice_url` — ссылки для оплаты через разные интерфейсы.
- `created_at` / `expiration_date` — время создания и истечения срока действия инвойса.

>**P.S.:** В примере `main.py` и в проекте Tezer используется интерфейс `mini_app_invoice_url`.

**Пример обработки JSON-ответа:**
```python
invoice = await rctz.open_invoice(amount=3, asset="TRX")
if invoice.get("ok"):
    result = invoice["result"]
    print(f"Счёт #{result['invoice_id']} на сумму {result['amount']} {result['asset']} успешно создан.")
    print(f"Ссылка для оплаты: {result['mini_app_invoice_url']}")
else:
    print("Не удалось создать инвойс.")
```

**Что демонстрирует пример:**  
Пример показывает, как обработать ответ API при создании счёта: извлечь из JSON нужные поля и вывести пользователю информацию об успешно созданном инвойсе и ссылке на оплату.

## close_invoice — закрытие инвойса
### `close_invoice(invoice_id: int)`

**Описание метода:**  
Метод `close_invoice` используется для закрытия ранее созданного платёжного инвойса по его уникальному идентификатору. После вызова метода инвойс становится недоступен для оплаты. Этот метод отправляет POST-запрос к API и возвращает JSON-объект с результатом операции.

**Аргументы:**  
- `invoice_id` *(int)* — уникальный идентификатор инвойса, который требуется закрыть.

**Пример использования:**  
```python
result = await rctz.close_invoice(invoice_id=715877)
print(result)
```

**Что демонстрирует пример:**  
В примере вызывается метод закрытия инвойса с ID 715877. После успешного выполнения метод возвращает подтверждение закрытия счёта.

**Возвращает:**  
- `dict` — JSON-объект с результатом операции.

**Пример возвращаемого JSON:**  
```json
{
  "ok": true,
  "result": true
}
```

**Ключевые поля ответа:**  
- `ok` — флаг успешности ответа от сервера.  
- `result` — `True`, если инвойс был успешно закрыт. Если инвойс был не найден или не закрыт `result` — `False`.

**Пример обработки JSON-ответа:**  
```python
response = await rctz.close_invoice(invoice_id=715877)
if str(response["result"]) == "true":
    print("Инвойс успешно закрыт.")
else:
    print("Не удалось закрыть инвойс.")
```

**Что демонстрирует пример:**  
Пример показывает, как обработать ответ API, чтобы вывести сообщение об успешном закрытии инвойса или об ошибке при выполнении операции.

---

## 2.3 Пример использования с aiogram
В этом разделе приведён пример интеграции модуля **RCTZ** в Telegram-бот на базе **aiogram** (файл `main.py`). Пример демонстрирует полный поток: создание инвойса, отправка пользователю ссылки для оплаты, ожидание оплаты (проверка статуса) и отмена заказа.

> **Внимание:** В примере используются тестовые токены и testnet-URL. Перед запуском в продакшн замените токены и базовый URL на боевые значения.

### Короткая архитектура примера
1. Пользователь нажимает кнопку покупки — генерируется инвойс через `rctz.open_invoice`.
2. Бот сохраняет состояние `WaitingForPayment` через FSM и показывает кнопку для отмены заказа.
3. Запускается асинхронный процесс ожидания (`check_invoice`), который опрашивает API каждые 15 секунд.
4. Когда инвойс становится `paid` — бот обновляет сообщение и сбрасывает состояние. Если инвойс `expired` или не найден — сообщается об истечении времени.
5. При отмене заказа бот вызывает `rctz.close_invoice` и снимает состояние.

## 2.3.1 Основные функции main.py
Файл `main.py` содержит основную логику Telegram-бота, реализованного с использованием библиотеки **aiogram**. Этот бот позволяет пользователям покупать токены Tezer, создавая инвойсы через модуль **RCTZ**. Ниже приведено описание ключевых функций и обработчиков, используемых в `main.py`, с акцентом на взаимодействие с классом `TezerReplenish` из модуля `RCTZ`.

### 1. Инициализация бота и модуля RCTZ
```python
bot = Bot(get_json_token(get_path(['SystemForTezer'], 'api_tokens.json'), type_token="tzr_test_bot_api"))
dp = Dispatcher(storage=MemoryStorage())
rctz = TezerReplenish(get_json_token(get_path(['SystemForTezer'], 'api_tokens.json'), type_token="test_crypto_api"))
```

- `bot`: Экземпляр бота aiogram, инициализированный с тестовым API-токеном.
- `dp`: Диспетчер aiogram, который управляет обработкой сообщений и колбэков.
- `rctz`: Экземпляр класса `TezerReplenish` из модуля `RCTZ`, используемый для взаимодействия с API.

### 2. Определение состояний FSM
```python
class PaymentStates(StatesGroup):
    WaitingForPayment = State()
```

- `PaymentStates`: Группа состояний, используемая для управления состоянием пользователя во время процесса оплаты. Состояние `WaitingForPayment` указывает, что пользователь ожидает оплаты инвойса.

### 3. Обработчик команды /start
```python
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    if await state.get_state() == PaymentStates.WaitingForPayment.state:
        await message.answer("⚠ У вас есть активный заказ! Завершите или отмените его.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buy 5 Tezer 💸", callback_data="buy_5")],
            [InlineKeyboardButton(text="Buy 1 Tezer 💸", callback_data="buy_1")]
        ]
    )
    await message.answer("Выберите количество Tezer для покупки:", reply_markup=keyboard)
```

- Этот обработчик срабатывает при получении команды `/start`. Он проверяет, находится ли пользователь в состоянии `WaitingForPayment`. Если да, то предупреждает пользователя о необходимости завершить или отменить текущий заказ. В другом случае, отображает кнопки для покупки 5 или 1 Tezer.

### 4. Обработчик покупки Tezer
Ниже представлена подробная документация для обработчика покупки токенов Tezer в Telegram-боте, реализованного с использованием библиотеки **aiogram**. Этот раздел предназначен для разработчиков, которые будут изучать, поддерживать или модифицировать данный код. Документация включает полный разбор кода, описание каждого шага и пояснения по взаимодействию с внешними компонентами.

#### Код обработчика
```python
@dp.callback_query(lambda c: c.data in ["buy_5", "buy_1"])
async def buy_tezer(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state() == PaymentStates.WaitingForPayment.state:
        await callback.answer("⚠ У вас уже есть активный заказ. Завершите или отмените его.", show_alert=True)
        return

    async def create_pay(amount: float, asset: str, description: str):
        invoice_data = await rctz.open_invoice(amount=amount, asset=asset, description=description)
        if not invoice_data["ok"]:
            await callback.message.answer("⚠ Ошибка при создании ордера. Попробуйте позже.")
            return

        amount_bot = 5 if callback.data == "buy_5" else 1
        invoice_id = invoice_data["result"]["invoice_id"]
        payment_url = invoice_data["result"]["mini_app_invoice_url"]
        await state.set_state(PaymentStates.WaitingForPayment)

        cancel_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Close a purchase order ❌", callback_data=f"cancel_{invoice_id}")]]
        )
        await callback.message.edit_text(
            f"✅ Ордер создан\n💳 Для пополнения кошелька на {amount_bot} Tezer \nПерейдите по ссылке: \n{payment_url}",
            reply_markup=cancel_keyboard
        )
        await check_payment(callback.from_user.id, invoice_id, callback.message.message_id, state)

    if callback.data == "buy_5":
        await create_pay(amount=3, asset='TRX', description="Replenishment of Tezer wallet for 3 TRX")
    elif callback.data == "buy_1":
        await create_pay(amount=0.1, asset='TON', description="Replenishment of Tezer wallet for 0.1 TON")
```

#### Общее описание
Обработчик `buy_tezer` активируется, когда пользователь нажимает на кнопки с данными `buy_5` или `buy_1`, соответствующими покупке 5 или 1 токена Tezer. Основная задача функции — создать инвойс для оплаты, отобразить пользователю ссылку на оплату и запустить процесс мониторинга статуса оплаты. Код использует асинхронные операции и FSM (Finite State Machine) для управления состоянием пользователя, что обеспечивает надежность и отзывчивость бота.

#### Детальный разбор кода
1. **Декоратор и определение функции**
   - **`@dp.callback_query(lambda c: c.data in ["buy_5", "buy_1"])`**  
     Этот декоратор регистрирует функцию `buy_tezer` как обработчик для колбэк-запросов, где данные (`callback.data`) равны `"buy_5"` или `"buy_1"`. Это означает, что функция будет вызвана при нажатии на кнопки "Buy 5 Tezer" или "Buy 1 Tezer".
   - **`async def buy_tezer(callback: types.CallbackQuery, state: FSMContext):`**  
     Асинхронная функция принимает два параметра:
     - `callback`: Объект колбэк-запроса, содержащий информацию о нажатой кнопке и контексте сообщения.
     - `state`: Контекст состояния FSM, используемый для отслеживания текущего состояния пользователя.

2. **Проверка текущего состояния**
   - **`if await state.get_state() == PaymentStates.WaitingForPayment.state:`**  
     Проверяет, находится ли пользователь в состоянии `WaitingForPayment`. Это состояние указывает, что у пользователя уже есть активный заказ.
   - **`await callback.answer(...)`**  
     Если условие выполняется, отправляется всплывающее уведомление с текстом:  
     `"⚠ У вас уже есть активный заказ. Завершите или отмените его."`  
     Параметр `show_alert=True` отображает сообщение как модальное окно.
   - **`return`**  
     Выполнение функции завершается, чтобы предотвратить создание нового инвойса, пока текущий заказ не завершен.

3. **Внутренняя функция `create_pay`**
   - **`async def create_pay(amount: float, asset: str, description: str):`**  
     Определяет вложенную асинхронную функцию для создания инвойса. Параметры:
     - `amount`: Сумма платежа (например, 3 TRX или 0.1 TON).
     - `asset`: Валюта платежа (например, `"TRX"` или `"TON"`).
     - `description`: Описание платежа, передаваемое в API.
   - **`invoice_data = await rctz.open_invoice(...)`**  
     Вызывает метод `open_invoice` из объекта `rctz` (экземпляра класса `TezerReplenish`), который отправляет запрос к API для создания инвойса. Возвращает словарь с данными инвойса.
   - **`if not invoice_data["ok"]:`**  
     Проверяет успешность создания инвойса. Если `"ok"` равно `False`, отправляется сообщение об ошибке:  
     `"⚠ Ошибка при создании ордера. Попробуйте позже."`, и выполнение функции завершается.

4. **Обработка данных инвойса**
   - **`amount_bot = 5 if callback.data == "buy_5" else 1`**  
     Определяет количество токенов Tezer, которое пользователь хочет купить: 5 для `"buy_5"`, 1 для `"buy_1"`.
   - **`invoice_id = invoice_data["result"]["invoice_id"]`**  
     Извлекает уникальный идентификатор инвойса из ответа API.
   - **`payment_url = invoice_data["result"]["mini_app_invoice_url"]`**  
     Извлекает URL для оплаты, который будет показан пользователю.

5. **Установка состояния и создание клавиатуры**
   - **`await state.set_state(PaymentStates.WaitingForPayment)`**  
     Устанавливает состояние пользователя в `WaitingForPayment`, чтобы отметить, что процесс оплаты начался.
   - **`cancel_keyboard = InlineKeyboardMarkup(...)`**  
     Создает инлайн-клавиатуру с одной кнопкой:  
     - Текст: `"Close a purchase order ❌"`.  
     - Данные колбэка: `"cancel_{invoice_id}"`, где `invoice_id` — уникальный идентификатор инвойса.  
     Эта кнопка позволяет пользователю отменить заказ.

6. **Редактирование сообщения**
   - **`await callback.message.edit_text(...)`**  
     Редактирует исходное сообщение, на которое был нажат колбэк. Новый текст:  
     ```
     ✅ Ордер создан
     💳 Для пополнения кошелька на {amount_bot} Tezer 
     Перейдите по ссылке: 
     {payment_url}
     ```  
     - `{amount_bot}`: Количество Tezer (5 или 1).  
     - `{payment_url}`: Ссылка для оплаты.  
     Параметр `reply_markup=cancel_keyboard` добавляет кнопку отмены к сообщению.

7. **Запуск проверки оплаты**
   - **`await check_payment(callback.from_user.id, invoice_id, callback.message.message_id, state)`**  
     Запускает асинхронную задачу `check_payment`, которая будет периодически проверять статус инвойса. Параметры:
     - `callback.from_user.id`: ID пользователя Telegram.
     - `invoice_id`: ID инвойса.
     - `callback.message.message_id`: ID сообщения, которое нужно обновлять.
     - `state`: Контекст FSM для управления состоянием.

8. **Выбор параметров оплаты**
   - **`if callback.data == "buy_5": await create_pay(...)`**  
     Если нажата кнопка `"buy_5"`, вызывает `create_pay` с параметрами:  
     - `amount=3` (3 TRX).  
     - `asset='TRX'`.  
     - `description="Replenishment of Tezer wallet for 3 TRX"`.
   - **`elif callback.data == "buy_1": await create_pay(...)`**  
     Если нажата кнопка `"buy_1"`, вызывает `create_pay` с параметрами:  
     - `amount=0.1` (0.1 TON).  
     - `asset='TON'`.  
     - `description="Replenishment of Tezer wallet for 0.1 TON"`.

#### Взаимодействие с модулем RCTZ
- **Создание инвойса**  
  Метод `rctz.open_invoice` из класса `TezerReplenish` отправляет запрос к API Tezer для создания инвойса. Он принимает параметры `amount`, `asset` и `description` и возвращает словарь с полями:  
  - `"ok"`: Булево значение, указывающее на успех операции.  
  - `"result"`: Словарь с данными инвойса, включая `invoice_id` и `mini_app_invoice_url`.

- **Проверка статуса оплаты**  
  Функция `check_payment` (предположительно определена в другом разделе кода) использует метод `rctz.check_invoice` для периодической проверки статуса инвойса по его `invoice_id`. Это позволяет боту автоматически реагировать на успешную оплату или другие изменения статуса.

#### Пример работы
1. Пользователь нажимает кнопку "Buy 5 Tezer".
2. Бот проверяет, что у пользователя нет активного заказа.
3. Создается инвойс на 3 TRX с описанием "Replenishment of Tezer wallet for 3 TRX".
4. Пользователю отображается сообщение:  
   ```
   ✅ Ордер создан
   💳 Для пополнения кошелька на 5 Tezer 
   Перейдите по ссылке: 
   [URL для оплаты]
   ```  
   с кнопкой "Close a purchase order ❌".
5. Запускается `check_payment` для мониторинга статуса оплаты.

### 5. Обработчик отмены заказа
```python
@dp.callback_query(lambda c: c.data.startswith("cancel_"))
async def cancel_order(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state() is None:
        await callback.answer("У вас нет активных заказов.", show_alert=True)
        return

    await rctz.close_invoice(int(callback.data.split("_")[1]))
    await state.clear()
    await callback.message.edit_text("❌ Ордер отменен.")
```

- Этот обработчик срабатывает при нажатии на кнопку отмены заказа. Он проверяет, есть ли активный заказ, и если да, то закрывает инвойс с помощью метода `rctz.close_invoice` и очищает состояние.

### 6. Функция проверки оплаты
```python
async def check_payment(user_id: int, invoice_id: int, message_id: int, state: FSMContext):
    if await rctz.check_invoice(invoice_id):
        await bot.edit_message_text("✅ Кошелек пополнен", chat_id=user_id, message_id=message_id)
    else:
        await bot.edit_message_text("⏳ Время на пополнение истекло.", chat_id=user_id, message_id=message_id)

    await state.clear()
```

- Эта функция проверяет статус инвойса с помощью метода `rctz.check_invoice`, который периодически опрашивает API. Если инвойс оплачен, редактирует сообщение, чтобы сообщить о пополнении кошелька. В противном случае, сообщает о истечении времени. В любом случае, очищает состояние.

### 7. Основной блок
```python
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
```

- Запускает polling бота, чтобы он мог получать и обрабатывать обновления от Telegram.

### Примечания
- **Использование модуля RCTZ**: В файле `main.py` активно используются методы класса `TezerReplenish` из модуля `RCTZ`:
  - `open_invoice`: Для создания нового инвойса.
  - `close_invoice`: Для отмены инвойса.
  - `check_invoice`: Для проверки статуса инвойса.
- **FSM (Finite State Machine)**: Используется для управления состояниями пользователя, что позволяет предотвратить одновременное выполнение нескольких операций.

> **Тестовый режим**: В текущей реализации используются тестовые токены и тестовый URL. Для продакшн-версии необходимо заменить их на боевые значения.

---

# 3. Модуль ExchangeCurrencyTezer (ECTZ)

## 3.1.1 AuthTransaction.db

**Описание файла:**  
`AuthTransaction.db` — это файл базы данных SQLite, используемый модулем **ExchangeCurrencyTezer (ECTZ)** для хранения информации о завершённых транзакциях.  
База данных служит для учёта пополнений и позволяет отслеживать историю операций, совершённых пользователями.

**Структура базы данных:**  
Таблица хранит записи о транзакциях с следующими столбцами:
- `id` *(INTEGER, PRIMARY KEY, AUTOINCREMENT)* — сквозной идентификатор записи в базе данных.  
- `id_transaction` *(TEXT)* — идентификатор транзакции, полученный от внешней системы после успешного проведения оплаты.  
- `amount` *(TEXT)* — сумма пополнения. 
- `currency` *(TEXT)* — валюта, в которой было произведено пополнение (например, `"RUB"`, `"USD"`, `"EUR"`).  
- `address` *(TEXT)* — адрес кошелька, на который было произведено пополнение.  

**Пример содержимого базы данных:**  
| id | id_transaction | address                 | amount | currency |
|----|----------------|-------------------------|--------|----------|
| 1  | 123456789      | TuFFEHttWmVNes1uQcpGtt | 10.0   | RUB      |

**Что демонстрирует пример:**  
Пример иллюстрирует запись о транзакции, в которой:  
- В таблицу добавлена запись с `id = 1`.  
- Уникальный идентификатор транзакции `123456789`.  
- Пополнение было выполнено на адрес `TuFFEHttWmVNes1uQcpGtt`.  
- Сумма пополнения составила `10.0` единиц.  
- Валюта пополнения — `RUB`.  

Таким образом, данная база данных является учётным журналом успешных пополнений, которые были подтверждены и записаны системой.
