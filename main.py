import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database import init_db

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    print("Бот запущен")
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

