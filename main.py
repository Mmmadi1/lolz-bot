import os
import asyncio
from aiohttp import web # Добавляем веб-сервер, чтобы Render не усыпал
import google.generativeai as genai
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STR = os.environ.get("SESSION_STR", "")
GEMINI_KEY = os.environ.get("GEMINI_KEY", "")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    if event.out:
        return
    try:
        await asyncio.sleep(2) # Задержка, чтоб не выглядеть роботом
        resp = model.generate_content(event.raw_text)
        await event.reply(resp.text)
    except Exception as ex:
        print("НЕРЕАЛИСТИЧНО:", ex)

# Мини-сервер для Render (пинг)
async def handle(request):
    return web.Response(text="Пишечка жива, лотяга!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер запущен на порту {port}")

async def main():
    await start_web_server()
    await client.start()
    print("Пишечка-бот запущен, лотяга. Знатнячок.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
