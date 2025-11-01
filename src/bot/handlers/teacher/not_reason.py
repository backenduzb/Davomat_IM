from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from bot.states.user import TeacherStates
from bot.database.student import (
    get_student_id,
)
from bot.database.teacher import (
    get_teacher_information
)
from bot.keyboards.inline.button import (
    finish_or_continue,
    finish
)
from bot.keyboards.reply.student import (
    students_keyboard
)

router = Router()

@router.callback_query(F.data == "have_no_reason_teacher")
async def finish_no_reason(callback: types.CallbackQuery, state: FSMContext):
    teacher = await get_teacher_information(teacher_id=str(callback.from_user.id))
    
    await state.set_state(TeacherStates.waiting_no_reason_student)
    await callback.message.answer(
        f"🏫 <b>{teacher.get('class_name')}</b> sinfidagi sababsiz kelmaganlarni kiriting.",
        reply_markup=await students_keyboard(callback.from_user.id)
    )

    await callback.answer()

@router.message(TeacherStates.waiting_no_reason_student)
async def reason_students(message: types.Message, state: FSMContext):
    
    student_name = message.text.strip()
    teacher_id = str(message.from_user.id)

    data = await state.get_data()
    no_reason_students = data.get("no_reason_students", [])

    if student_name not in no_reason_students:
        no_reason_students.append(student_name)

    await state.update_data({"no_reason_students": no_reason_students})

    teacher = await get_teacher_information(teacher_id)
    class_name = teacher.get("class_name", "Noma'lum sinf")

    students_text = "\n".join([f"• {name}" for name in no_reason_students])

    await message.answer(
        f"🏫 <b>{class_name}</b> sinfi bo‘yicha sababsiz kelmagan o‘quvchilar:\n\n{students_text}",
        reply_markup=await finish_or_continue("no_reason_teacher")
    )

    await message.answer(
        "Yana o'quvchi qo'shmoqchi bolsangiz o'quvchisingizni tanlang.",
        reply_markup=await students_keyboard(message.from_user.id)
    )
@router.callback_query(F.data == "finish_no_reason_teacher")
async def finish_no_reason(callback: types.CallbackQuery, state: FSMContext):
    teacher = await get_teacher_information(str(callback.from_user.id))
    await callback.message.answer(
        f"<b>{teacher.get("teacher_name")}</b> sababli kelgan o'quvchilar bormi?",
        reply_markup=await finish(inf="reason_teacher")
    )
    await state.set_state(None)

    await callback.answer()

@router.callback_query(F.data=="clear_no_reason_teacher")
async def clear_reason(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(no_reason_students=[])
    await callback.answer("Sababsiz o'quvchilar ro'yhati tozalandi.", show_alert=True)
    teacher = await get_teacher_information(teacher_id=str(callback.from_user.id))

    await state.set_state(TeacherStates.waiting_no_reason_student)
    await callback.message.answer(
        f"🏫 <b>{teacher.get('class_name')}</b> sinfidagi sababsiz kelmaganlarni kiriting.",
        reply_markup=await students_keyboard(callback.from_user.id)
    )

    await callback.answer()