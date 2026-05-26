import requests
from datetime import datetime
import os

EVENT_URL = "https://tixcraft.com/activity/detail/26_joji"
API_URL = "https://tixcraft.com/ticket/area/26_joji/22381"

LINE_TOKEN = os.getenv("LINE_TOKEN")

session = requests.Session()

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    "Referer": EVENT_URL,
    "Origin": "https://tixcraft.com",
}


def send_line(msg):
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={
            "Authorization": f"Bearer {LINE_TOKEN}"
        },
        data={
            "message": msg
        }
    )


def init_cookie():
    session.get(
        "https://tixcraft.com",
        headers=headers,
        timeout=15
    )

    session.get(
        EVENT_URL,
        headers=headers,
        timeout=15
    )


def check_ticket():
    r = session.get(
        API_URL,
        headers=headers,
        timeout=20
    )

    print("status:", r.status_code)

    if r.status_code != 200:
        print(r.text)
        return

    data = r.json()

    areas = data.get("areas", [])

    available = []

    for area in areas:
        name = area.get("areaName", "")
        remain = area.get("remain", 0)

        if int(remain) > 0:
            available.append(
                f"{name} 剩餘 {remain} 張"
            )

    if available:
        msg = (
            f"有票啦！\n\n"
            f"{datetime.now()}\n\n"
            + "\n".join(available)
            + f"\n\n{EVENT_URL}"
        )

        print(msg)

        send_line(msg)

    else:
        print("目前沒票")


if __name__ == "__main__":
    init_cookie()
    check_ticket()
