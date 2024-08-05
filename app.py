import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from database.engine import create_db, session_maker, drop_db

from handlers.main import user_private_router

from keyboards.main_menu import set_main_menu
from middlewares.db import DataBaseSession

logger = logging.getLogger(__name__)

config: Config = load_config()

bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
dp = Dispatcher()

dp.include_router(user_private_router)

async def on_startup(bot):

    await drop_db()

    await create_db()

async def on_shutdown(bot):
    print('Бот лег!')


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '               
                               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))   #сессия на все хэндлеры
    await bot.send_message(config.tg_bot.id_admin, text='Бот запущен!')
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) # передеаем все виды апдеййтов. если что-то хотим заблочить то можно передать сюда.

asyncio.run(main())
