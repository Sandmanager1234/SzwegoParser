#!/usr/bin/python3.9
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from keyboard import create_main_keyboard, create_back_keyboard
from datechecker import check_date
from aiogram.types import FSInputFile
import traceback


import os
from shop_parser.parser import collect_data

parse = Router()

categories = {
    'Часы': 'A2017122802434822429',
    'Кроссовки': 'A2017120822295108026', 
    'Сумки': 'A201803280031209720038067', 
    'Одежда': 'A2018031702370069766',
    'Артикулы': 'A2018030720290279534',
    'Артикулы 2': 'A201908281438457360129101'
}


class WhatToParse(StatesGroup):
    set_date = State()
    download = State()


@parse.message(Command(commands=['start']))
async def bot_start(msg: types.Message):
    await msg.answer('Что парсим?', reply_markup=create_main_keyboard())


@parse.message(WhatToParse.set_date)
async def type_date(msg: types.Message, state: FSMContext):
    await state.update_data(start_date=msg.text)
    date = msg.text
    if msg.text == "Назад":
        await msg.answer('Выберите категорию.', reply_markup=create_main_keyboard())
        await state.clear()
    else:
        if await check_date(date, msg) == True:
            await state.set_state(WhatToParse.download)
            try:
                await download_files(msg, state)
            except Exception as ex:
                print(traceback.format_exc())
                await msg.answer(f'Что-то пошло не так. Ошибка: {ex}', reply_markup=create_main_keyboard())
                await msg.answer('Выберите категорию')
                await state.clear()
        else:
            await msg.answer('Неправильно введённая дата. Попробуйте ещё раз.', reply_markup=create_back_keyboard())


async def download_files(msg: types.Message, state: FSMContext):
    hui = await state.get_data()
    message = await msg.answer('Начинается загрузка.')
    await collect_data(hui['album'], hui['start_date'], message)
    await message.edit_text('Загрузка окончена.')
    if len(os.listdir('tables')) != 0:
        for table in os.listdir('tables'):
            file = FSInputFile(f'tables/{table}')
            await msg.answer_document(file)
            os.remove(f'tables/{table}')
    else:
        await msg.answer('Подходящих товаров не нашлось.')
    await msg.answer('Можете начать заново.', reply_markup=create_main_keyboard())
    await state.clear()


@parse.message()
async def choose_category(msg: types.message, state: FSMContext):
    if msg.text in categories:
        await msg.answer('Отлично!', reply_markup=ReplyKeyboardRemove)
        await state.update_data(album=categories[f'{msg.text}'])
        await msg.answer('Введите дату начала парсинга в формате гггг-мм-дд. Пример: 2022-12-31.', reply_markup=create_back_keyboard())
        await state.set_state(WhatToParse.set_date)
    else:
        await msg.answer('Неправильная категория. Попробуйте другую.', reply_markup=create_main_keyboard())



