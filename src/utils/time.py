from datetime import datetime

import pytz


def current_time():
    uz_tz = pytz.timezone("Asia/Tashkent")
    now_date = datetime.now(uz_tz)
    return now_date.strftime("%Y/%m/%d")
