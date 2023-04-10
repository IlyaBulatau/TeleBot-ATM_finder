from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON

def create_choice_bank_kb():
    keyboard = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=val, callback_data=key) for key, val in LEXICON.items()]
    keyboard.row(*buttons)
    return keyboard.as_markup()

def create_get_location_user():
    button = KeyboardButton(text='Отправить геоданные', request_location=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], one_time_keyboard=True, resize_keyboard=True)
    return keyboard

