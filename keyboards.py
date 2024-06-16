from aiogram.dispatcher.filters import Text
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram import types
from aiogram.utils.callback_data import CallbackData

import db
from main import dp

web_app = WebAppInfo(url='https://ohsudden.github.io/')

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Grocery Store', web_app=web_app)]
    ],
    resize_keyboard=True
)
cb = CallbackData('btn', 'action')
key = InlineKeyboardMarkup(
    incline_keyboard=[[InlineKeyboardButton('Pay', callback_data='btn:buy')]]
)


