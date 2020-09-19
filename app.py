from loader import bot
from config import ADMIN


async def on_shutdown(dp):
	await bot.send_message(chat_id=ADMIN, text="Бот окончил свою работу")
	await bot.close()

async def send_to_admin(dp):
	await bot.send_message(chat_id=ADMIN, text="Бот запущен")


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=send_to_admin, on_shutdown=on_shutdown)