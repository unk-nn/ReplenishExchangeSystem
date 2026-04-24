import peewee as pw
from GetPathToken import get_path

# Подключение к SQLite базе данных (файл AuthTransaction.db)
#открытие базу данных через файл. База общая TezerPlatform, две таблицы TezerPerson и AuthTransaction
db = pw.SqliteDatabase(get_path(['SystemForTezer', 'SystemsPay', 'ReplenishExchangeSystem','ExchangeCurrencyTezer', 'DataBase'], 'AuthTransaction.db'))

# Модель таблицы AuthTransaction
class AuthTransactionAllerts(pw.Model):
    id = pw.IntegerField(column_name='id', primary_key=True)
    transaction = pw.CharField(column_name='id_transaction', unique=True, null=False)
    address = pw.CharField(column_name='address', null=False)
    amount = pw.CharField(column_name='amount', null=False)
    currency = pw.CharField(column_name='currency', null=False)

    class Meta:
        database = db
        table_name = "AuthTransaction"

# Устанавливаем соединение с БД
db.connect()
