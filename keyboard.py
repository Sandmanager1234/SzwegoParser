#!/usr/bin/python3.9
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

kb = [
    [
        types.KeyboardButton(text='Часы'),
        types.KeyboardButton(text='Кроссовки'),
        types.KeyboardButton(text='Одежда'),
        types.KeyboardButton(text='Сумки'),
    ],
    [
        types.KeyboardButton(text='Артикулы'),
        types.KeyboardButton(text='Артикулы 2')
    ]
]
kb2 = [
    [
        types.KeyboardButton(text='Назад'),
    ]
]


def create_main_keyboard():
    builder = ReplyKeyboardBuilder(kb).adjust(2)
    return builder.as_markup()

def create_back_keyboard():
    builder = ReplyKeyboardBuilder(kb2).adjust(1)
    
    return builder.as_markup()