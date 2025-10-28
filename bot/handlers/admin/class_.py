from aiogram  import Router, types, F
from bot.states.user import AdminStates
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline.button import (
    finish
)

router = Router()

@router.message(AdminStates.waiting_class)
async def waiting_class(message: types.Message, state: FSMContext):
    class_name = message.text.strip()
    await state.update_data(class_name=class_name)
    
    await message.answer(
        "Sababsiz kelmagan o‘quvchilar bormi?",
        reply_markup=await finish(inf="no_reason_admin")
    )

