from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='My wallets')],
    [KeyboardButton(text='See stats')],
    [KeyboardButton(text='Add wallet')]
],
    resize_keyboard=True,
    input_field_placeholder='Choose option')

menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Back to menu', callback_data='main_menu')]
    ]
)

wallet = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Stats')],
    [KeyboardButton(text='Update')],
    [KeyboardButton(text='Delete')],
    [KeyboardButton(text='Back')]
])

async def build_reply_keyboard(list: list):
    keyboard = ReplyKeyboardBuilder()
    keyboard = [[KeyboardButton(text=item)] for item in list]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def build_inline_keyboard(list: list):
    keyboard = InlineKeyboardBuilder()
    for l in list:
        keyboard.add(
            InlineKeyboardButton(
                text=l,
                callback_data=l
            )
        )
        print(l)
    return keyboard.adjust(4).as_markup()





