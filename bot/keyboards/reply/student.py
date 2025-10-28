from bot.database.student import get_students_by_teacher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def students_keyboard(teacher_id: str)->ReplyKeyboardMarkup:
    students = await get_students_by_teacher(teacher_id)  

    buttons = [students[i:i+2] for i in range(0, len(students), 2)]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=s) for s in row] for row in buttons],
        resize_keyboard=True
    )
    return keyboard