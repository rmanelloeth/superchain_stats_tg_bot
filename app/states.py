from aiogram.fsm.state import StatesGroup, State


from aiogram.fsm.state import State, StatesGroup

class WalletState(StatesGroup):
    address = State()


