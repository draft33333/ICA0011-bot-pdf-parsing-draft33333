from aiogram.fsm.state import StatesGroup, State


class ParsePDFState(StatesGroup):
    waiting_for_pdf = State()
