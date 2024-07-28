from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from keyboards import get_main_kb, get_city_kb
from parse_weather import get_weather
from config.config import load_config
import db

from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon import COMMANDS

storage = MemoryStorage()
router = Router()


class FSMFillForm(StatesGroup):
    fill_city = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=COMMANDS['start'],
                         reply_markup=get_main_kb(),
                         parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'city', StateFilter(default_state))
async def city_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Введите город\nВаш выбранный город: {db.get_city_by_user_id(callback.from_user.id)}",
                                  reply_markup=get_city_kb())
    await state.set_state(FSMFillForm.fill_city)
    await callback.message.delete()


@router.callback_query(F.data == 'weather')
async def weather_callback(callback: CallbackQuery):
    city = db.get_city_by_user_id(callback.from_user.id)
    if not city:
        await callback.message.answer("Вы еще не выбрали город!\nНажмите на кнопку <b>Изменить город</b>",
                                      reply_markup=get_main_kb(),
                                      parse_mode=ParseMode.HTML)
        await callback.message.delete()
    else:
        weather_info = get_weather(city, load_config().api_id)
        await callback.message.answer(weather_info, reply_markup=get_main_kb())
        await callback.message.delete()


@router.message(StateFilter(FSMFillForm.fill_city), F.text.isalpha())
async def fill_city(message: CallbackQuery, state: FSMContext):
    db.add_user_city(message.from_user.id, message.text)
    await message.answer("Город записан!", reply_markup=get_main_kb())
    await message.delete()
    await state.clear()


@router.callback_query(F.data == 'cancel', StateFilter(FSMFillForm.fill_city))
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await start(callback.message)
    await callback.message.delete()


@router.message(StateFilter(FSMFillForm.fill_city))
async def warning_fill_city(message: Message):
    await message.answer('То, что вы отправили не похоже на город'
                         '\nПожалуйста, введите корректные данные',
                         reply_markup=get_city_kb())
    await message.delete()


@router.message()
async def weather_fill_city(message: Message):
    await message.answer("Я не понимаю вас!", reply_markup=get_main_kb())
    await message.delete()
