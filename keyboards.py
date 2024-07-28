from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_kb() -> InlineKeyboardMarkup:
    btn_city = InlineKeyboardButton(text="Изменить город", callback_data="city")
    btn_weather = InlineKeyboardButton(text="Узнать погоду", callback_data="weather")
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn_city], [btn_weather]])

    return kb


def get_city_kb() -> InlineKeyboardMarkup:
    btn_cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn_cancel]])

    return kb
