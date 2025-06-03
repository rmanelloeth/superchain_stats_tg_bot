import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN

from app.handlers import router

bot = Bot(TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    #Logging юзать только при разработке, вырубать при работе
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
