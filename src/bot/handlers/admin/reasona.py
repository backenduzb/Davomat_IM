from aiogram import Router, types, F
from bot.database.admin import get_admin_tg_ids, get_student_id
from bot.keyboards.reply.admin import all_students
from bot.keyboards.reply.student import reastart
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from bot.states.user import AdminStates
from bot.keyboards.inline.button import (
    finish_or_continue,
    finish
)
from bot.database.student import edit_student_no_reason, edit_student_reason


router = Router()

@router.callback_query(F.data == "have_reason_admin")
async def choose_reason_students(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await state.set_state(AdminStates.waiting_reason_student)
    await callback.message.answer(
        f"🏫 <b>{data.get('class_name')}</b> sinfidagi <b>sababli kelmagan</b> o‘quvchilarni tanlang 👇",
        reply_markup=await all_students(data.get('class_name'))
    )
    await callback.answer()

@router.message(AdminStates.waiting_reason_student)
async def ask_reason(message: types.Message, state: FSMContext):
    student_name = message.text.strip()
    data = await state.get_data()

    reason_students = data.get("reason_students", {})
    no_reason_students = data.get("no_reason_students", {})
    
    if student_name not in reason_students and student_name not in no_reason_students:
        reason_students[student_name] = None

        await state.update_data(reason_students=reason_students, current_student=student_name)
        await message.answer(f"📋 <b>{student_name}</b> nima sababdan darsga kelmadi? ✏️")
        await state.set_state(AdminStates.waiting_reason)
    else:
        await message.answer(
            "Iltimos boshqa o'quvchi tanlang. Chunk bu o'quvchi allaqachon ro'yhatda."
        )

@router.message(AdminStates.waiting_reason)
async def save_reason(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_student = data.get("current_student")
    reason_students = data.get("reason_students", {})

    reason_students[current_student] = message.text.strip()
    await state.update_data(reason_students=reason_students)

    class_name = data.get("class_name", "Noma'lum sinf")

    students_text = "\n".join([
        f"🟡 <b>{name}</b> — <i>{reason}</i>" for name, reason in reason_students.items()
    ])

    await message.answer(
        f"✅ <b>{current_student}</b> sabab saqlandi.\n\n"
        f"🏫 <b>{class_name}</b> sinfidagi hozircha sababli kelmaganlar:\n\n{students_text}",
        reply_markup=await finish_or_continue("reason_admin")
    )
    await message.answer(
        "Yana o'quvchi qo'shmoqchi bolsangiz o'quvchisingizni tanlang.",
        reply_markup=await all_students(class_name)
    )
    
    await state.set_state(None)
    await state.set_state(AdminStates.waiting_reason_student)

@router.callback_query(F.data == "finish_reason_admin")
async def finish_reason_list(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await state.clear()

    reason_students = data.get("reason_students", {})  
    no_reason_students = data.get("no_reason_students", [])  

    class_name = data.get('class_name')

    for name in no_reason_students:
        try:
            student_id = await get_student_id(name, class_name)
            await edit_student_no_reason(student_id)
        except Exception as e:
            print(f"❌ Xatolik sababsiz: {name} -> {e}")

    for name, reason in reason_students.items():
        try:
            student_id = await get_student_id(name, class_name)
            await edit_student_reason(student_id, "Sababli dars qoldirgan", reason)
        except Exception as e:
            print(f"❌ Xatolik sababli: {name} -> {e}")

    no_reason_text = "🚫 Sababsizlar yo‘q." if not no_reason_students else "\n".join(
        [f"❌ <i>{name}</i>" for name in no_reason_students]
    )
    reason_text = "🟡 Sabablilar yo‘q." if not reason_students else "\n".join(
        [f"💤 <b>{name}</b> — <i>{reason}</i>" for name, reason in reason_students.items()]
    )

    await callback.message.answer(
        f"📊 <b>{class_name}</b> sinfi bo‘yicha kelmaganlar ma’lumotlari yangilandi ✅\n\n"
        f"🚫 <b>Sababsizlar:</b>\n{no_reason_text}\n\n"
        f"🟡 <b>Sabablilar:</b>\n{reason_text}",
        reply_markup=await reastart()
    )

@router.callback_query(F.data=="clear_reason_admin")
async def clear_reason(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(reason_students={})
    data = await state.get_data
    await callback.answer("Sababli o'quvchilar ro'yhati tozalandi.", show_alert=True)
    

    await state.set_state(AdminStates.waiting_reason_student)
    await callback.message.answer(
        f"🏫 <b>{data.get('class_name')}</b> sinfidagi <b>sababli kelmagan</b> o‘quvchilarni tanlang 👇",
        reply_markup=await all_students(data.get('class_name'))
    )

    await callback.answer()