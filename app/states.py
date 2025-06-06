from aiogram.fsm.state import StatesGroup, State


from aiogram.fsm.state import State, StatesGroup

class WalletState(StatesGroup):
    add_wallet = State()
    add_label = State()
    info = State()
    current_wallet = State()




