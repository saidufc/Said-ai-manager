import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM = """
Ты — SAID AI, менеджер по работе с клиентами.

Отвечай на русском, таджикском, английском и китайском.
Автоматически определяй язык клиента.

Наши услуги:
START — от 1500 рублей.
PRO — от 5000 рублей.
BUSINESS — от 10000 рублей.

Помогай клиентам, консультируй и принимай заявки.
Не придумывай цены и обещания.
Если клиент хочет заказать услугу, предложи связаться с Саидом.
Будь вежливым и профессиональным.
"""

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Здравствуйте! Я SAID AI 👋\n"
        "Помогу вам с вопросами о создании Telegram-ботов."
    )

@dp.message(Command("clear"))
async def clear(message: Message):
    await message.answer("Начнём новый разговор!")

@dp.message(F.chat.type == "private", F.text)
async def answer(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")

    try:
        response = await asyncio.to_thread(
            ai.chat.completions.create,
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": message.text}
            ],
            max_tokens=500
        )

        text = response.choices[0].message.content
        await message.answer(text or "Попробуйте задать вопрос ещё раз.")

    except Exception:
        logging.exception("AI error")
        await message.answer("Извините, возникла техническая ошибка.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
