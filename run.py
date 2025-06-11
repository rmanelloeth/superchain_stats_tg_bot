import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN

from app.handlers import router

bot = Bot(TOKEN)
dp = Dispatcher()



def load_proxies(path: str = "proxy.txt") -> list[str]:
    with open(path, "r") as f:
        lines = f.readlines()
    return [f"http://{line.strip().replace(':', ':', 1)}" for line in lines if line.strip()]

async def main():
    dp.include_router(router)
    proxies = load_proxies()
    dp.workflow_data["proxies"] = proxies
    await dp.start_polling(bot)

if __name__ == '__main__':
    #Logging юзать только при разработке, вырубать при работе
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
