from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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

