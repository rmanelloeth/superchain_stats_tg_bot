from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from app.utils import get_tx_counts_all_chains
from app.states import WalletState
import operations

router = Router()

async def send_main_menu(message: Message):
    await message.answer("Backed to main menu", reply_markup=kb.main)

@router.message(CommandStart())
async def cmd_start(message: Message):
    ids = operations.get_user_ids()
    if str(message.from_user.id) not in ids:
        operations.add_new_user(str(message.from_user.id),str(message.from_user.username))
    await message.reply("Привет, я помогу тебе собрать статистику Superchain", reply_markup=kb.main)

@router.message(F.text == 'My wallets')
async def cmd_wallet(message: Message, state: FSMContext):
    ...
    await state.set_state(WalletState.address)
    await message.answer('Input wallet')

@router.message(F.text == 'Add wallet')
async def add_wallet(message: Message, state: FSMContext):
    await state.set_state(WalletState.add_wallet)
    await message.answer('Input wallet')

@router.message(WalletState.add_wallet)
async def input_wallet(message: Message, state: FSMContext):
    address = message.text.strip()
    await state.update_data(add_wallet=address)
    exists = operations.add_new_wallet(str(message.from_user.id),str(address))
    if exists == False:
        await message.reply(f'Добавил в БД кошелек: {address}', reply_markup=kb.menu)
        await state.clear()
    else:
        await message.reply(f'Такой кошелек уже есть!', reply_markup=kb.menu)
        await state.clear()


@router.callback_query(F.data =='main_menu')
async def back_to_main_menu(query: CallbackQuery ):
    await query.answer()
    await send_main_menu(query.message)

@router.message(WalletState.info)
async def get_wallet_info(message: Message, state: FSMContext):
    address = message.text.strip()
    await state.update_data(info=address)

    tx_dict = await get_tx_counts_all_chains(address)

    # Формируем читаемый ответ
    lines = [f"<b>📊 Транзакции по адресу:</b> <code>{address}</code>\n"]
    for chain_id, txs in tx_dict.items():
        name = CHAIN_NAMES.get(chain_id, f"Chain {chain_id}")
        lines.append(f"• <b>{name}</b>: {txs}")

    response = "\n".join(lines)
    await message.answer(response, parse_mode="HTML")
    await state.clear()
