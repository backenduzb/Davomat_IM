from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.database.admin import set_class_students_null
from bot.database.student import (
    edit_student_no_reason,
    edit_student_reason,
    get_student_id,
)
from bot.database.teacher import get_teacher_information
from bot.keyboards.inline.button import finish, finish_or_continue
from bot.keyboards.reply.student import reastart, students_keyboard
from bot.states.user import TeacherStates

router = Router()


@router.callback_query(F.data == "have_reason_teacher")
async def choose_reason_students(callback: types.CallbackQuery, state: FSMContext):
    teacher = await get_teacher_information(teacher_id=str(callback.from_user.id))

    await state.set_state(TeacherStates.waiting_reason_student)
    await callback.message.answer(
        f"🏫 <b>{teacher.get('class_name')}</b> sinfidagi <b>sababli kelmagan</b> o‘quvchilarni tanlang 👇",
        reply_markup=await students_keyboard(callback.from_user.id),
    )
    await callback.answer()


@router.message(TeacherStates.waiting_reason_student)
async def ask_reason(message: types.Message, state: FSMContext):
    student_name = message.text.strip()
    data = await state.get_data()

    reason_students = data.get("reason_students", {})
    no_reason_students = data.get("no_reason_students", {})

    if student_name not in reason_students and student_name not in no_reason_students:
        reason_students[student_name] = None

        await state.update_data(
            reason_students=reason_students, current_student=student_name
        )
        await message.answer(
            f"📋 <b>{student_name}</b> nima sababdan darsga kelmadi? ✏️"
        )
        await state.set_state(TeacherStates.waiting_reason)
    else:
        await message.answer(
            "Iltimos boshqa o'quvchi tanlang. Chunk bu o'quvchi allaqachon ro'yhatda."
        )


@router.message(TeacherStates.waiting_reason)
async def save_reason(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_student = data.get("current_student")
    reason_students = data.get("reason_students", {})

    reason_students[current_student] = message.text.strip()
    await state.update_data(reason_students=reason_students)

    teacher = await get_teacher_information(str(message.from_user.id))
    class_name = teacher.get("class_name", "Noma'lum sinf")

    students_text = "\n".join(
        [
            f"🟡 <b>{name}</b> — <i>{reason}</i>"
            for name, reason in reason_students.items()
        ]
    )

    await message.answer(
        f"✅ <b>{current_student}</b> sabab saqlandi.\n\n"
        f"🏫 <b>{class_name}</b> sinfidagi hozircha sababli kelmaganlar:\n\n{students_text}",
        reply_markup=await finish_or_continue("reason_teacher"),
    )
    await message.answer(
        "Yana o'quvchi qo'shmoqchi bolsangiz o'quvchisingizni tanlang.",
        reply_markup=await students_keyboard(message.from_user.id),
    )

    await state.set_state(None)
    await state.set_state(TeacherStates.waiting_reason_student)


@router.callback_query(F.data == "finish_reason_teacher")
async def finish_reason_list(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await state.clear()

    reason_students = data.get("reason_students", {})
    no_reason_students = data.get("no_reason_students", [])

    teacher_id = str(callback.from_user.id)
    teacher = await get_teacher_information(teacher_id)
    class_name = teacher.get("class_name", "Noma'lum sinf")
    await set_class_students_null(class_name)
    for name in no_reason_students:
        try:
            student_id = await get_student_id(name, teacher_id)
            await edit_student_no_reason(student_id)
        except Exception as e:
            print(f"❌ Xatolik sababsiz: {name} -> {e}")

    for name, reason in reason_students.items():
        try:
            student_id = await get_student_id(name, teacher_id)
            await edit_student_reason(student_id, "Sababli dars qoldirgan", reason)
        except Exception as e:
            print(f"❌ Xatolik sababli: {name} -> {e}")

    no_reason_text = (
        "🚫 Sababsizlar yo‘q."
        if not no_reason_students
        else "\n".join([f"❌ <i>{name}</i>" for name in no_reason_students])
    )
    reason_text = (
        "🟡 Sabablilar yo‘q."
        if not reason_students
        else "\n".join(
            [
                f"💤 <b>{name}</b> — <i>{reason}</i>"
                for name, reason in reason_students.items()
            ]
        )
    )

    from utils.time import current_time

    now_uz = current_time()

    oylar = {
        "January": "yanvar",
        "February": "fevral",
        "March": "mart",
        "April": "aprel",
        "May": "may",
        "June": "iyun",
        "July": "iyul",
        "August": "avgust",
        "September": "sentyabr",
        "October": "oktyabr",
        "November": "noyabr",
        "December": "dekabr",
    }

    oy_nomi = oylar[now_uz.strftime("%B")]
    formatted_date = now_uz.strftime(f"%Y-yil %d-{oy_nomi}")

    await callback.message.answer(
        f"📊 <b>{class_name}</b> sinfi bo‘yicha kelmaganlar ma’lumotlari yangilandi ✅\n\n"
        f"🚫 <b>Sababsizlar:</b>\n{no_reason_text}\n\n"
        f"🟡 <b>Sabablilar:</b>\n{reason_text}"
        f"{formatted_date}da oxirgi marta yangilandi.",
        reply_markup=await reastart(),
    )


@router.callback_query(F.data == "clear_reason_teacher")
async def clear_reason(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(reason_students={})
    await callback.answer("Sababli o'quvchilar ro'yhati tozalandi.", show_alert=True)
    teacher = await get_teacher_information(teacher_id=str(callback.from_user.id))

    await state.set_state(TeacherStates.waiting_reason_student)
    await callback.message.answer(
        f"🏫 <b>{teacher.get('class_name')}</b> sinfidagi <b>sababli kelmagan</b> o‘quvchilarni tanlang 👇",
        reply_markup=await students_keyboard(callback.from_user.id),
    )

    await callback.answer()
