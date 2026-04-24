import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from RCTZ import TezerReplenish
from GetPathToken import get_json_token, get_path

# Перед официальном использовании заменить API tokens и в RCTZ url на url без testnet
bot = Bot(get_json_token(get_path(['SystemForTezer'], 'api_tokens.json'), type_token="tzr_test_bot_api"))
dp = Dispatcher(storage=MemoryStorage())
rctz = TezerReplenish(get_json_token(get_path(['SystemForTezer'], 'api_tokens.json'), type_token="test_crypto_api"))

# Определение состояний FSM
class PaymentStates(StatesGroup):
    WaitingForPayment = State()

# --- ГЛАВНОЕ МЕНЮ ---
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

# --- ОБРАБОТКА КНОПОК ПОКУПКИ ---
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
        await state.set_state(PaymentStates.WaitingForPayment)  # Устанавливаем состояние ожидания оплаты

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

# --- ОТМЕНА ПОКУПКИ ---
@dp.callback_query(lambda c: c.data.startswith("cancel_"))
async def cancel_order(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state() is None:
        await callback.answer("У вас нет активных заказов.", show_alert=True)
        return

    close = await rctz.close_invoice(int(callback.data.split("_")[1]))
    print(close)
    await state.clear()
    await callback.message.edit_text("❌ Ордер отменен.")

# --- ПРОВЕРКА ОПЛАТЫ ---
async def check_payment(user_id: int, invoice_id: int, message_id: int, state: FSMContext):
    if await rctz.check_invoice(invoice_id):
        await bot.edit_message_text("✅ Кошелек пополнен", chat_id=user_id, message_id=message_id)
    else:
        await bot.edit_message_text("❌ Ордер закрыт.", chat_id=user_id, message_id=message_id)

    await state.clear()  # Сбрасываем состояние

# @dp.message() # Необходимо в основной версии tezer, чтобы не приходилось на каждую кнопку или действие вешать блокировку
# async def block_commands(message: types.Message, state: FSMContext):
#     if await state.get_state() == PaymentStates.WaitingForPayment.state:
#         await message.answer("🚫 Завершите покупку перед выполнением других команд!")
#         return

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))