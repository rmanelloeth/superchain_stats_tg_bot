from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from app.utils import get_base_tx_count
from app.states import WalletState

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Привет, я помогу тебе собрать статистику Superchain \n"
                         "пришли номер кошелька", reply_markup=kb.main)

@router.message(F.text == 'wallet')
async def cmd_wallet(message: Message, state: FSMContext):
    await state.set_state(WalletState.address)
    await message.answer('Input wallet')

@router.message(WalletState.address)
async def get_wallet_info(message: Message, state: FSMContext):
    await state.update_data(address = message.text)
    tx_count = await get_base_tx_count(message.text)
    await message.answer(text=f'Количество транзакций в сети Base: {tx_count} на кошельке {message.text}')
