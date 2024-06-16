from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import ParseMode, KeyboardButton, ReplyKeyboardMarkup

from main import bot, dp
from keyboards import keyboard
from aiogram import types
from aiogram.dispatcher.filters import Command
import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
import db
from aiogram.dispatcher.filters import Text

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Працює Grocery Store',
                           reply_markup=keyboard)


PRICE = {
    '1': [types.LabeledPrice(label='Item1', amount=10)],
    '2': [types.LabeledPrice(label='Item2', amount=200000)],
    '3': [types.LabeledPrice(label='Item3', amount=300000)],
    '4': [types.LabeledPrice(label='Item4', amount=400000)],
    '5': [types.LabeledPrice(label='Item5', amount=500000)],
    '6': [types.LabeledPrice(label='Item6', amount=600000)]
}

PAYMENT_TOKEN = '1877036958:TEST:3dd6fdaceb0084a89d3912077322a5e02d646d72'
@dp.message_handler(content_types='web_app_data')
async def buy_process(web_app_message):
    await bot.send_invoice(web_app_message.chat.id,
                           title='Food',
                           description='Description',
                           provider_token=PAYMENT_TOKEN,
                           currency='usd',
                           need_email=True,
                           prices=PRICE[f'{web_app_message.web_app_data.data}'],
                           start_parameter='example',
                           payload='some_invoice')


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Платіж успішно виконаний!')


user_last_login = {}


class Form(StatesGroup):
    daily_bonus = State()


@dp.message_handler(Command('login'))
async def daily_login_bonus(message: types.Message):
    user_id = message.from_user.id
    current_time = datetime.datetime.utcnow()

    # Check if the user logged in today
    if user_id in user_last_login:
        last_login_time = user_last_login[user_id]
        if (current_time - last_login_time).days == 0:
            await message.reply("You have already received your daily bonus today!")
            return


    user_last_login[user_id] = current_time

    daily_bonus_amount = 0.05


    await message.reply(f"Congratulations! You've received a daily bonus of {daily_bonus_amount} TON!")


@dp.message_handler(commands=['balance'])
@dp.message_handler(Text(equals='balance', ignore_case=True))
async def balance_handler(message: types.Message):
    uid = message.from_user.id

    # Get user balance from database
    user_balance = db.get_balance(uid)
    if user_balance is None:
        user_balance = 0  # Handle the case where the balance is None

    # Convert from nanoton to TON (1 TON = 1e9 nanoton)
    user_balance = user_balance / 1e9

    # Format balance and send to user
    await message.answer(f'Your balance: *{user_balance:.2f} TON*',
                         parse_mode=ParseMode.MARKDOWN)

