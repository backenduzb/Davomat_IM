from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.database.teacher import get_all_teachers_id, get_teacher_information
from bot.database.admin import get_admin_tg_ids, get_all_no
from bot.keyboards.reply.admin import all_class
from bot.keyboards.inline.button import finish
from bot.states.user import TeacherStates, AdminStates
from bot.keyboards.reply.student import reastart


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Assalomu alaykum <b>{message.from_user.full_name}</b> 👋",
                         reply_markup=await reastart()
                         )


@router.message(F.text == "Davomat topshirish 📝")
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = str(message.from_user.id)

    teacher_ids = await get_all_teachers_id()
    admin_ids = await get_admin_tg_ids()

    if user_id in admin_ids:
        await message.answer(f"Assalomu alaykum <b>{message.from_user.full_name}</b> 👋")

        data = await get_all_no()
        
        if not data:
            await message.answer("📭 Hozircha hech qanday dars qoldirgan o‘quvchilar yo‘q.")
        else:
            summary = data.pop("_summary", None)
            text = "📊 <b>Sinf kesimidagi yo‘qlar ro‘yxati</b>\n\n"

            for class_name, info in data.items():
                if info["reason"] or info["no_reason"]:
                    text += f"🏫 <b>{class_name}</b> — {info['present_percent']}% o‘quvchi kelgan\n"

                if info["reason"]:
                    text += "\n🟡 <b>Sababli yo‘qlar:</b>\n"
                    for i, s in enumerate(info["reason"], start=1):
                        sababi = s["sababi"] or "Sabab ko‘rsatilmagan"
                        text += f"{i}. {s['full_name']} — <i>{sababi}</i>\n"

                if info["no_reason"]:
                    text += "\n🔴 <b>Sababsiz yo‘qlar:</b>\n"
                    for i, s in enumerate(info["no_reason"], start=1):
                        sababi = s["sababi"] or "Sabab ko‘rsatilmagan"
                        text += f"{i}. {s['full_name']} — <i>{sababi}</i>\n"

                text += "\n"

            if summary:
                from django.utils import timezone
                import pytz

                uz_tz = pytz.timezone("Asia/Tashkent")
                now_uz = timezone.now().astimezone(uz_tz)

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



                text += (
                    f"📅 <b>{formatted_date} kungi davomat haqida MAʼLUMOT</b>\n\n"
                    f"Jami: <b>{summary['total_students']}</b> nafar o‘quvchi\n"
                    f"Shundan <b>{summary['total_absent']}</b> nafari kelmagan\n"
                    f"{summary['total_reason']} nafari sababli\n"
                    f"{summary['total_no_reason']} nafari sababsiz\n\n"
                    f"Umumiy: <b>{summary['total_present_percent']}%</b>\n"
                )

            await message.answer(text)


        await message.answer("Iltimos, to‘ldirish uchun sinfni tanlang 👇", reply_markup=await all_class())
        await state.set_state(AdminStates.waiting_class)

    elif user_id in teacher_ids:
        teacher = await get_teacher_information(user_id)
        await message.answer(
            f"Assalomu alaykum <b>{teacher.get('teacher_name')}</b> 👋\n"
            f"Bugungi davomad jarayonini boshlaymiz.\n\n"
            f"Sababsiz kelmagan o‘quvchilar bormi?",
            reply_markup=await finish(inf='no_reason_teacher')
        )
        await state.set_state(TeacherStates.waiting_no_reason_student)

    else:
        await message.answer(f"<b>{message.from_user.full_name}</b>! Afsuski siz davomat topshira olmaysiz.")
