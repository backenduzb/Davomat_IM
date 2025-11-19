import requests
from datetime import datetime
import pytz

uz_tz = pytz.timezone("Asia/Tashkent")
now_date = datetime.now(uz_tz)
now_caption = now_date.strftime("%Y/%m/%d")  

BOT_TOKEN = "7102026834:AAFnKJiSiecmgd_giX25CzeTRGAvf1ec0Zs"
GROUP_ID = "-1003013595617"

def upload_document(document):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    data = {
        "chat_id": GROUP_ID,
        "caption": f"📅 Sana: {now_caption}"
    }

    with open(document, "rb") as file:
        response = requests.post(url, data=data, files={"document": file})

    if response.status_code == 200:
        print("✅ Fayl muvaffaqiyatli yuborildi!")
    else:
        print(f"❌ Xatolik: {response.status_code}")
        print(response.text)
