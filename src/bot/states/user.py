from aiogram.fsm.state import State, StatesGroup

class TeacherStates(StatesGroup):
    waiting_reason_student = State()
    waiting_no_reason_student = State()
    waiting_finish_no_reason = State()
    waiting_finish_reason = State()
    waiting_reason = State()

class AdminStates(StatesGroup):
    waiting_class = State()
    waiting_reason_student = State()
    waiting_no_reason_student = State()
    waiting_finish_no_reason = State()
    waiting_finish_reason = State()
    waiting_reason = State()
