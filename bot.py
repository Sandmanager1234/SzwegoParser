#!/usr/bin/python3.9
import logging
import asyncio
from handlers import parsing_chat
from keyboard import *
from aiogram import Bot, Dispatcher


# from configs.config import config
from configs.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)


async def main():
    dp = Dispatcher()
    dp.include_router(parsing_chat.parse)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())