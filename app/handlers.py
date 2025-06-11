from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from typing import Literal
from app.proxies import proxies

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
    # await message.answer("text", reply_markup=ReplyKeyboardRemove())
    ids = operations.get_user_ids()
    if str(message.from_user.id) not in ids:
        operations.add_new_user(str(message.from_user.id),str(message.from_user.username))
    await message.answer("📊 <b>Superchain Stats Bot</b>\n"
    "Base · OP · Ink · Lisk · Unichain · Mode", reply_markup=kb.main, parse_mode='HTML')
@router.callback_query(F.data == 'add_wallet')
async def add_wallet(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WalletState.add_label)
    await callback.message.edit_text('Введи номер аккаунта', reply_markup=kb.menu)

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
        await message.answer(f'Добавил в БД кошелек: {address}', reply_markup=kb.menu)
        await state.clear()
    else:
        await message.answer(f'Такой кошелек уже есть!', reply_markup=kb.menu)
        await state.clear()


@router.callback_query(F.data =='main_menu')
async def back_to_main_menu(query: CallbackQuery, state: FSMContext):
    await state.set_state(WalletState.main_menu)
    await query.answer()
    await send_main_menu(query.message)

@router.callback_query(F.data == 'my_wallets')
async def get_wallets_info(callback: CallbackQuery):
    wallets, labels = operations.get_user_wallets(str(callback.from_user.id))
    if not wallets:
        await callback.message.answer('У вас еще нет добавленных кошельков', reply_markup=kb.menu)
    else:
        await callback.message.edit_text('Ваши кошельки', reply_markup= await kb.build_inline_keyboard(wallets,labels))

@router.callback_query(F.data.startswith("wallet "))
async def wallet_actions(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    label, wallet = callback.data.split("|", 2)
    await state.set_state(WalletState.current_wallet)
    await state.update_data(current_wallet=wallet)
    await state.update_data(current_label=label)
    await callback.message.edit_text(text=f'{label} menu\n{wallet}',reply_markup=kb.wallet)

@router.callback_query(F.data == 'stats')
async def get_wallet_stats(callback:CallbackQuery,state: FSMContext):
    data = await state.get_data()
    wallet = data.get('current_wallet')
    label = data.get('current_label')
    stats = operations.get_wallet_stat(wallet)
    if not stats:
        await callback.message.edit_text('У этого кошелька нет статистики', reply_markup=kb.back_to_wallets)
    else:
        stats = stats[0]
        text = (
            f"<b>Стата для кошелька {label}</b>\n\n"
            f"<a href=\"https://debank.com/profile/{wallet}?chain=\">{wallet}</a>\n\n"
            f"<b>Optimism:</b> {stats[2]}\n"
            f"<b>Base:</b> {stats[3]}\n"
            f"<b>Ink:</b> {stats[4]}\n"
            f"<b>Soneium:</b> {stats[5]}\n"
            f"<b>Lisk:</b> {stats[6]}\n"
            f"<b>Unichain:</b> {stats[7]}\n"
            f"<b>Mode:</b> {stats[8]}"
        )
        await callback.message.edit_text(text=text, reply_markup=kb.back_to_wallets, parse_mode='HTML',disable_web_page_preview=True)

@router.callback_query(F.data == 'update')
async def update_stat(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    wallet = data.get('current_wallet')
    label = data.get('current_label')
    results = await get_tx_counts_all_chains(wallet, proxies)
    operations.update_stat(str(callback.from_user.id), wallet, results)
    await callback.message.edit_text(f'Обновил стату для кошелька: {label}\n{wallet}',reply_markup=kb.back_to_wallets)

@router.callback_query(F.data == 'delete')
async def delete_wallet(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    wallet = data.get('current_wallet')
    label = data.get('current_label')
    operations.delete_wallet(wallet, str(callback.from_user.id))
    await callback.message.edit_text(f'Удалил кошелек {label}\n\n{wallet}', reply_markup=kb.main)

@router.callback_query(F.data == 'see_stats')
async def see_all_stats(callback: CallbackQuery):
    wallets, labels = operations.get_user_wallets(callback.from_user.id)
    all_stats = []
    for wallet, label in zip(wallets, labels):
        stats = operations.get_wallet_stat(wallet)
        all_stats.append((label,wallet,stats))

    has_data = any(stat for _, _, stat in all_stats)

    if not has_data:
        await callback.message.edit_text(
            "<b>Нет доступной статистики по кошелькам.</b>", reply_markup=kb.menu,
            parse_mode="HTML"
        )
        return

    header = f"{'Label':<10} {'Wallet':<42} {'OPT':>5} {'BASE':>5} {'INK':>5} {'SONEIUM':>5} {'LISK':>5} {'UNI':>5} {'MODE':>5} "
    rows = [header, "-" * len(header)]

    for label, wallet, stat_data in all_stats:
        if not stat_data:
            # Если нет данных — ставим прочерки
            row = f"{label:<10} {wallet:<42} {'-':>5} {'-':>5} {'-':>5} {'-':>5} {'-':>5} {'-':>5} {'-':>5}"
        else:
            stat = stat_data[0]  # первая строка
            row = f"{label:<10} {wallet:<42} {stat[2]:>5} {stat[3]:>5} {stat[4]:>5} {stat[5]:>5} {stat[6]:>5} {stat[7]:>5} {stat[8]:>5}"
        rows.append(row)

    text = "<pre>\n" + "\n".join(rows) + "\n</pre>"

    await callback.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=kb.menu)

@router.callback_query(F.data == 'update_all_stats')
async def update_all_stats(callback: CallbackQuery):
    wallets, labels=operations.get_user_wallets(str(callback.from_user.id))
    for wallet, label in zip(wallets, labels):
        results = await get_tx_counts_all_chains(wallet, proxies)
        operations.update_stat(str(callback.from_user.id), wallet, results)
        await callback.message.edit_text(f'Обновляю стату для кошелька: {label}\n{wallet}',
                                         reply_markup=kb.back_to_wallets)
    await callback.message.edit_text("📊 <b>Обновил стату для всех кошельков</b>\n",
                                     parse_mode='HTML',reply_markup=kb.main)

















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
