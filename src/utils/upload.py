import requests

from bot.config.settings import BOT_TOKEN, GROUP_ID, ARCHIVE_GROUP

from .time import current_time
import time

def upload_document_archive(document_path: str):
    today = current_time()

    data = {
        "chat_id": ARCHIVE_GROUP,
        "caption": f"📅 Sana: {today}",
    }

    with open(document_path, "rb") as f:
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
            data=data,
            files={"document": f},
            timeout=60,
        )

    if resp.status_code == 200:
        return True
    else:
        return False

def upload_document(document_path: str):
    today = current_time()

    archived = upload_document_archive(document_path)
    time.sleep(0.5)

    archived_mark = "✅" if archived else "❌"

    caption = (
        f"<b>📅 Sana:</b> <code>{today}</code>\n"
        f"<b>📦 Arxivlangan:</b> {archived_mark}"
    )

    data = {
        "chat_id": GROUP_ID,
        "caption": caption,
        "parse_mode": "HTML",
    }

    with open(document_path, "rb") as f:
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
            data=data,
            files={"document": f},
            timeout=60,
        )

    if resp.status_code == 200:
        print("✅ Fayl muvaffaqiyatli yuborildi!")
    else:
        print(f"❌ Xatolik: {resp.status_code}")
        print(resp.text)

