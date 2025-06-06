from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from typing import Literal

import app.keyboards as kb

from app.utils import get_tx_counts_all_chains
from app.states import WalletState
import operations

router = Router()


async def send_main_menu(message: Message):
    await message.edit_text("📊 <b>Superchain Stats Bot</b>\n"
    "Base · OP · Ink · Lisk · Unichain", reply_markup=kb.main, parse_mode='HTML')


@router.message(CommandStart())
async def cmd_start(message: Message):
    ids = operations.get_user_ids()
    if str(message.from_user.id) not in ids:
        operations.add_new_user(str(message.from_user.id),str(message.from_user.username))
    await message.answer("📊 <b>Superchain Stats Bot</b>\n"
    "Base · OP · Ink · Lisk · Unichain", reply_markup=kb.main, parse_mode='HTML')
@router.callback_query(F.data == 'add_wallet')
async def add_wallet(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WalletState.add_label)
    await callback.message.edit_text('Введи номер аккаунта')

@router.message(WalletState.add_label)
async def input_label(message: Message, state: FSMContext):
    label = message.text.strip()
    await state.update_data(add_label=label)
    await state.set_state(WalletState.add_wallet)
    await message.answer('Введине адрес кошелька')

@router.message(WalletState.add_wallet)
async def input_wallet(message: Message, state: FSMContext):
    address = message.text.strip()
    await state.update_data(add_wallet=address)
    data = await state.get_data()
    exists = operations.add_new_wallet(str(message.from_user.id),str(data.get("add_wallet")),str(data.get("add_label")))
    if exists == False:
        await message.reply(f'Добавил в БД кошелек: {address}', reply_markup=kb.menu)
        await state.clear()
    else:
        await message.reply(f'Такой кошелек уже есть!', reply_markup=kb.menu)
        await state.clear()


@router.callback_query(F.data =='main_menu')
async def back_to_main_menu(query: CallbackQuery):
    await query.answer()
    await send_main_menu(query.message)

@router.callback_query(F.data == 'my_wallets')
async def get_wallets_info(callback: CallbackQuery):
    wallets, labels = operations.get_user_wallets(str(callback.from_user.id))
    if not wallets:
        await callback.message.reply('У вас еще нет добавленных кошельков')
    else:
        await callback.message.edit_text('Ваши кошельки', reply_markup= await kb.build_inline_keyboard(wallets,labels))


@router.callback_query(F.data.startswith("wallet "))
async def wallet_actions(callback: CallbackQuery, state: FSMContext):
    label, wallet = callback.data.split("|", 2)
    await state.set_state(WalletState.current_wallet)
    await state.update_data(current_wallet=wallet)
    await callback.message.edit_text(text=f'{label} menu\n{wallet}',reply_markup=kb.wallet)

@router.callback_query(F.data == 'stats')
async def get_wallet_stats(callback:CallbackQuery,state: FSMContext):
    data = await state.get_data()
    wallet = data.get('current_wallet')
    if not wallet:
        await callback.message.edit_text(f'Для кошелька {wallet} требуется обновить статистику')






# @router.message(F.text == 'My wallets')
# async def get_wallet_info(message: Message, state: FSMContext):
#     address = message.text.strip()
#     await state.update_data(info=address)
#
#     tx_dict = await get_tx_counts_all_chains(address)
#
#     # Формируем читаемый ответ
#     lines = [f"<b>📊 Транзакции по адресу:</b> <code>{address}</code>\n"]
#     for chain_id, txs in tx_dict.items():
#         name = CHAIN_NAMES.get(chain_id, f"Chain {chain_id}")
#         lines.append(f"• <b>{name}</b>: {txs}")
#
#     response = "\n".join(lines)
#     await message.answer(response, parse_mode="HTML")
#     await state.clear()
