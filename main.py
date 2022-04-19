import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from config import BOT_TOKEN

loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, loop=loop, storage=storage)


if __name__ == "__main__":
    from handlers import dp, send_greeting_to_admin
    executor.start_polling(dp, on_startup=send_greeting_to_admin, skip_updates=True)




