from aiogram import Router, types, F
from bot.database.admin import get_admin_tg_ids
from bot.keyboards.reply.admin import all_students
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from bot.states.user import AdminStates
from bot.keyboards.inline.button import (
    finish_or_continue,
    finish
)

router = Router()

@router.callback_query(F.data == "have_no_reason_admin")
async def have_reason(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data.get("class_name"))
    await callback.message.answer(
        "O'quvchilardan birini tanlang.",
        reply_markup=await all_students(data.get("class_name"))
    )
    await state.set_state(AdminStates.waiting_no_reason_student)
    await callback.answer()

@router.message(AdminStates.waiting_no_reason_student)
async def reason_students(message: types.Message, state: FSMContext):
    
    student_name = message.text.strip()

    data = await state.get_data()
    no_reason_students = data.get("no_reason_students", [])

    if student_name not in no_reason_students:
        no_reason_students.append(student_name)

    await state.update_data({"no_reason_students": no_reason_students})

    class_name = data.get("class_name")

    students_text = "\n".join([f"• {name}" for name in no_reason_students])

    await message.answer(
        f"🏫 <b>{class_name}</b> sinfi bo‘yicha sababsiz kelmagan o‘quvchilar:\n\n{students_text}",
        reply_markup=await finish_or_continue("no_reason_admin")
    )

    await message.answer(
        "Yana o'quvchi qo'shmoqchi bolsangiz o'quvchisingizni tanlang.",
        reply_markup=await all_students(data.get("class_name"))
    )

@router.callback_query(F.data == "finish_no_reason_admin")
async def finish_no_reason(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"Sabasli kelgan o'quvchilar bormi?",
        reply_markup=await finish(inf="reason_admin")
    )
    await state.set_state(None)

    await callback.answer()

@router.callback_query(F.data=="clear_no_reason_admin")
async def clear_reason(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(no_reason_students=[])
    await callback.answer("Sababli o'quvchilar ro'yhati tozalandi.", show_alert=True)
    data = await state.get_data()
    await state.set_state(AdminStates.waiting_no_reason_student)
    await callback.message.answer(
        f"🏫 <b>{data.get('class_name')}</b> sinfidagi sababsiz kelmaganlarni kiriting.",
        reply_markup=await all_students(data.get('class_name'))
    )

    await callback.answer()


