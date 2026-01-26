import requests
from bot.config.settings import BOT_TOKEN, GROUP_ID
from .time import current_time

def upload_document(document_path: str):
    today = current_time()

    data = {
        "chat_id": GROUP_ID,
        "caption": f"📅 Sana: {today}",
    }

    with open(document_path, "rb") as f:
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
            data=data,
            files={"document": f},
            timeout=60
        )

    if resp.status_code == 200:
        print("✅ Fayl muvaffaqiyatli yuborildi!")
    else:
        print(f"❌ Xatolik: {resp.status_code}")
        print(resp.text)
