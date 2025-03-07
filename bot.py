import asyncio
import sqlite3
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "TG_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def create_database():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            currency TEXT,
            last_price REAL,
            deviation REAL,
            UNIQUE(user_id, currency)
        )
    """)
    conn.commit()
    conn.close()

create_database()

async def get_usd_to_rub():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json(content_type=None)
            return data["Valute"]["USD"]["Value"]

async def get_p2p_price(currency):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={currency}USDT"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return float(data["price"])
            return None

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Я бот для отслеживания P2P курсов. Используйте /track <валюта> <процент>.")

@dp.message(Command("track"))
async def cmd_track(message: Message):
    args = message.text.split()[1:]
    if len(args) < 2:
        await message.answer("⚠️ Формат команды: /track <валюта> <процент>")
        return
    
    currency, deviation = args[0].upper(), args[1]
    try:
        deviation = float(deviation)
    except ValueError:
        await message.answer("⚠️ Процент отклонения должен быть числом.")
        return
    
    current_price = await get_p2p_price(currency)
    if current_price is None:
        await message.answer(f"⚠️ Не удалось получить цену для {currency}.")
        return

    user_id = message.from_user.id

    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tracking (user_id, currency, last_price, deviation)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, currency) DO UPDATE SET deviation = excluded.deviation
    """, (user_id, currency, current_price, deviation))
    conn.commit()
    conn.close()
    
    await message.answer(f"✅ {currency} добавлен в отслеживание! Оповещения при изменении ±{deviation}%.")

async def check_price_task():
    while True:
        conn = sqlite3.connect("tracker.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, currency, last_price, deviation FROM tracking")
        rows = cursor.fetchall()
        
        usd_to_rub = await get_usd_to_rub()
        
        for user_id, currency, last_price, deviation in rows:
            new_price = await get_p2p_price(currency)
            if new_price is None:
                continue

            percent_change = ((new_price - last_price) / last_price) * 100 if last_price else 0
            percent_change = round(percent_change, 3)

            if abs(percent_change) >= deviation:
                price_rub = round(new_price * usd_to_rub, 2)
                message = (
                    f"🚨 Цена {currency} изменилась на {percent_change}%!\n"
                    f"🔹 Было: {last_price} USDT\n"
                    f"🔸 Сейчас: {new_price} USDT ({price_rub} RUB)"
                )
                await bot.send_message(user_id, message)

                cursor.execute("UPDATE tracking SET last_price = ? WHERE user_id = ? AND currency = ?", (new_price, user_id, currency))
                conn.commit()

        conn.close()
        await asyncio.sleep(10)

async def main():
    asyncio.create_task(check_price_task())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
