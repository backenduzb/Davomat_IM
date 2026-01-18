import os
import requests
from datetime import datetime
import pytz

from bot.config.settings import BOT_TOKEN, GROUP_ID


API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def _today_caption():
    uz_tz = pytz.timezone("Asia/Tashkent")
    now_date = datetime.now(uz_tz)
    return now_date.strftime("%Y/%m/%d")


def _already_sent_today(filename: str, today: str, limit: int = 50) -> bool:
    r = requests.get(f"{API}/getUpdates", timeout=20)
    if r.status_code != 200:
        return False
    data = r.json()
    if not data.get("ok"):
        return False

    updates = data.get("result", [])[-limit:]
    for upd in reversed(updates):
        msg = upd.get("message") or upd.get("channel_post") or {}
        chat = msg.get("chat", {})
        if str(chat.get("id")) != str(GROUP_ID) and chat.get("username") != str(GROUP_ID).lstrip("@"):
            continue

        doc = msg.get("document")
        if not doc:
            continue

        cap = msg.get("caption") or ""
        if doc.get("file_name") == filename and today in cap:
            return True

    return False


def upload_document(document_path: str):
    today = _today_caption()
    filename = os.path.basename(document_path)

    if _already_sent_today(filename, today):
        print(f"⏭️ Skip: '{filename}' bugun ({today}) allaqachon yuborilgan.")
        return

    url = f"{API}/sendDocument"
    data = {
        "chat_id": GROUP_ID,
        "caption": f"📅 Sana: {today}",
    }

    with open(document_path, "rb") as f:
        resp = requests.post(url, data=data, files={"document": f}, timeout=60)

    if resp.status_code == 200:
        print("✅ Fayl muvaffaqiyatli yuborildi!")
    else:
        print(f"❌ Xatolik: {resp.status_code}")
        print(resp.text)
