
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from collections import defaultdict
import os

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = "muinebikes"
MANAGER_LINK = "https://t.me/muinebikes"

referrals = defaultdict(list)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    args = message.get_args()
    user = message.from_user
    partner = args if args else "unknown"
    referrals[partner].append((user.id, user.username or "no_username"))
    await bot.send_message(f"@{ADMIN_USERNAME}",
        f"👤 Новый клиент от {partner}:
@{user.username or 'без username'}")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text="📩 Написать менеджеру", url=MANAGER_LINK))
    await message.answer(
        "Спасибо за обращение! Нажмите кнопку ниже, чтобы связаться с менеджером 👇",
        reply_markup=keyboard
    )

@dp.message_handler(commands=['stats'])
async def handle_stats(message: types.Message):
    partner = message.from_user.username
    records = referrals.get(partner, [])
    text = f"📊 Ваша статистика:
Переходов: {len(records)}"
    await message.answer(text)

@dp.message_handler(commands=['admin'])
async def handle_admin(message: types.Message):
    if message.from_user.username != ADMIN_USERNAME:
        await message.answer("⛔ Нет доступа.")
        return
    report = "📈 Общая статистика:
"
    for partner, users in referrals.items():
        report += f"• {partner}: {len(users)} переходов
"
    await message.answer(report or "Пока нет переходов.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
