from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def finish_or_continue(inf: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Tozalash 🗑", callback_data=f"clear_{inf}")],
        [InlineKeyboardButton(text="Tugatish ✅", callback_data=f"finish_{inf}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def finish(inf: str) -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton(text="Sababsizlarni kirtish ➕" if inf=="no_reason_admin" or inf=="no_reason_teacher" else "Sabablilarni kirtish ➕", callback_data=f"have_{inf}")],
        [InlineKeyboardButton(text="Sababsizlar yo'q ✅" if inf=="no_reason_admin" or inf=="no_reason_teacher" else "Sabalilar yo'q ✅", callback_data=f"finish_{inf}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=button)