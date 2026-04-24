import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from SystemForTezer.SystemsPay.ReplenishExchangeSystem.ExchangeCurrencyTezer.ECTZ import SystemExchangePay
from GetPathToken import get_json_token, get_path

bot = Bot(get_json_token(get_path(['SystemForTezer'], 'api_tokens.json'), type_token='tzr_test_bot_api'))
dp = Dispatcher(storage=MemoryStorage())
sep = SystemExchangePay(get_json_token(get_path(['SystemForTezer'], 'api_tokens.json'), type_token="alrt_active_access_token"))

class PaymentStates(StatesGroup):
    WaitingForPayment = State()

@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    if await state.get_state() == PaymentStates.WaitingForPayment.state:
        await message.answer("⚠ У вас есть активный заказ! Завершите или отмените его.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buy 1 Tezer 💸", callback_data="buy_1")]
        ]
    )
    await message.answer("Выберите количество Tezer для покупки:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data in ["buy_5", "buy_1"])
async def buy_tezer(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state() == PaymentStates.WaitingForPayment.state:
        await callback.answer("⚠ У вас уже есть активный заказ. Завершите или отмените его.", show_alert=True)
        return

    async def active_paymenets(amount:float, currency:str):
        await state.set_state(PaymentStates.WaitingForPayment)

        cancel_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Close a purchase order ❌", callback_data=f"cancel_order")]]
        )
        await callback.message.edit_text(
            f"✅ <b>Ордер создан</b>\n💳 Для пополнения кошелька на {amount} '{currency}' \nПерейдите по ссылке: \n https://www.donationalerts.com/r/tezerplatform \n <b>Следуйте инструкциям по оплате по ссылке</b>",
            reply_markup=cancel_keyboard, parse_mode="HTML"
        )

        status = await sep.open_invoice_allerts(int(callback.from_user.id), 'TuFFBHttWmVNns1uQcpGt', 10.0, 'RUB') #параметры от выбора пользователя в боте #здесь в тестовом режиме
        while not status.done():
            await asyncio.sleep(5)

        if status.result() == True:
            await state.clear()
            await callback.message.edit_text(
                f"✅ <b>Кошелек успешно пополнен</b>", parse_mode="HTML")
        elif status.result() == False:
            await state.clear()
            await callback.message.edit_text(
                f"❌ <b>Ордер закрыт</b>", parse_mode="HTML")
    if callback.data == "buy_1":
        await active_paymenets(10.0, 'RUB')

@dp.callback_query(lambda c: c.data.startswith("cancel_order"))
async def cancel_order(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state() is None:
        await callback.answer("У вас нет активных заказов.", show_alert=True)
        return

    await sep.close_invoice_allerts(callback.from_user.id)
    await state.clear()
    await callback.message.edit_text("❌ Ордер отменен.")

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))