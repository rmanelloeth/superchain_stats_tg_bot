from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='My wallets', callback_data='my_wallets')],
     [InlineKeyboardButton(text='See stats',callback_data='see_stats')],
    [InlineKeyboardButton(text='Add wallet',callback_data='add_wallet'),
     InlineKeyboardButton(text='Update all stats', callback_data='update_all_stats')]
])

menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Back to menu', callback_data='main_menu')]
    ]
)

wallet = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Stats', callback_data='stats'),
     InlineKeyboardButton(text='Update',callback_data='update'),
     InlineKeyboardButton(text='Delete',callback_data='delete'),
     InlineKeyboardButton(text='Back',callback_data='my_wallets')]
])

back_to_wallets = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Back', callback_data='my_wallets')]])

undo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Back', callback_data='main_menu')]])

async def build_inline_keyboard(wallets: list, labels: list):
    keyboard = InlineKeyboardBuilder()
    for wallet, label in zip(wallets,labels):
        keyboard.add(
            InlineKeyboardButton(
                text=label,
                callback_data=f'{label}|{wallet}'
            )
        )

    keyboard.add(InlineKeyboardButton(
                text='Back',
                callback_data='main_menu'
            ))
    return keyboard.adjust(4).as_markup()





