import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
MODEL = "llama-3.1-70b-versatile"  # 70B, чтоб лимитов хватило, 405B потом сам включишь

client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Йо, я Llama 70B через Groq. Пиши что угодно, без цензуры.")

@dp.message()
async def handle(message: types.Message):
    try:
        resp = await client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": message.text}],
            temperature=0.9,
            max_tokens=2048
        )
        await message.answer(resp.choices[0].message.content)
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def main():
    print("Бот запущен, сука")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
