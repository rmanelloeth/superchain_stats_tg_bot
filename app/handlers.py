from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router, F

import app.keyboards as kb

from app.utils import get_base_tx_count

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Привет, я помогу тебе собрать статистику Superchain \n"
                         "пришли номер кошелька", reply_markup=kb.main)

@router.message(F.text == 'wallet')
async def cmd_wallet(message: Message):
    txs, wallet = await get_base_tx_count('0xA795ecc5bF12A45C7F99ac16870d941D2c9Cd6dA')
    await message.reply(text=f'Количество транзакций в сети Base: {txs} на кошельке {wallet}  ')
