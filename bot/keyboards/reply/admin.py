from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.database.admin import get_all_class, get_students

async def all_class()->ReplyKeyboardMarkup:
    students = await get_all_class()  

    buttons = [students[i:i+5] for i in range(0, len(students), 5)]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=s) for s in row] for row in buttons],
        resize_keyboard=True
    )
    return keyboard

async def all_students(class_name)->ReplyKeyboardMarkup:
    students = await get_students(class_name)  

    buttons = [students[i:i+2] for i in range(0, len(students), 2)]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=s) for s in row] for row in buttons],
        resize_keyboard=True
    )
