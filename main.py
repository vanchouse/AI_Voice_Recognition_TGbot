import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
from database import init_db, add_user
from ai_logic import transcribe_voice, get_summary

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    await message.answer("Привет! Я твой AI-ассистент. Я уже записал тебя в свою базу данных. Отправь мне голосовое сообщение, я переведу его в текст и сделаю краткую выжимку")

@dp.message(F.voice)
async def voice_handler(message: types.Message, bot: Bot):
    await message.answer("Голосовое сообщение принято, загружаю...")

    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, 'voice.ogg')

    await  message.answer("Файл успешно скачан и сохранён, слушаю и перевожу...")
    text = transcribe_voice("voice.ogg")

    if text.startswith("Извини") or text.startswith("Ошибка"):
        await message.answer(text)
        return

    await message.answer("Читаю текст и делаю выжимку...")
    summary = get_summary(text)

    final_text = F"Распознаный текст:\n{text}\n\nКраткая выжимка:\n{summary}"

    await message.answer(final_text, parse_mode="HTML")

    try:
        os.remove("voice.ogg")
        os.remove("voice.wav")
    except Exception as e:
        print(F"Не смог удалить временные файлы: {e}")

async def main():
    await init_db()
    print("Бот запущен и база готова!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())