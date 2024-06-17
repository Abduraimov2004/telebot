import logging
from db import Database
from button import menu_keyboard, addresses_keyboard

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7202294382:AAEqrzzFPIQ3QH8O2ssuZOleRHDamU6U6JE"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Boshlang'ich Welcome habarini yuboradi va foydalanuvchini bazaga kiritadi yoki
    u allaqachon mavjud bo'lsa, Sizni yana ko'rganimdan xursandman xabarini qayta yuboradi
    """
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    username = message.from_user.username
    query = f"INSERT INTO users(username, full_name, user_id) VALUES('{username}', '{full_name}', {user_id})"
    if await Database.check_user_id(user_id):
        await message.reply(f"Sizni yana ko'rganimdan xursandman @{username}", reply_markup=menu_keyboard)
    else:
        await Database.connect(query, "insert")
        await message.reply(f"Welcome @{username}", reply_markup=menu_keyboard)

@dp.message_handler(lambda message: message.text == "Menyu")
async def menu(message: types.Message):
    """
    "Menyu" tugmasi bosilganda, menyularni ko'rsatadi
    """
    await message.answer("Menyular", reply_markup=addresses_keyboard)

@dp.message_handler(lambda message: message.text == "Back")
async def menu(message: types.Message):
    """
    "Back" tugmasi bosilganda, asosiy menyuni qayta ko'rsatadi
    """
    await message.answer("Menyular", reply_markup=menu_keyboard)

@dp.message_handler(lambda message: message.text == "1")
async def show_username(message: types.Message):
    """
    1 tugmasi bosilganda foydalanuvchi nomini ko'rsatadi    """
    await message.answer(f"Sizning username: @{message.from_user.username}")

@dp.message_handler(lambda message: message.text == "2")
async def show_user_id(message: types.Message):
    """
    2 tugmasi bosilganda, foydalanuvchi ID sini ko'rsatadi
    """
    await message.answer(f"Sizning user_id: {message.from_user.id}")

@dp.message_handler()
async def echo(message: types.Message):
    """
    Barcha boshqa xabarlarni qaytaradi
    (Foydalanuvchi nima yozsa oshani qaytaradi)
    """
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
