from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='wallet')]
], resize_keyboard=True, input_field_placeholder = 'Choose option')


