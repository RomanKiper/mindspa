from aiogram.filters import Filter
from aiogram import types, Bot
from config_data.config import Config, load_config

config: Config = load_config()

class IsAdminMsg(Filter):
    def __init__(self) -> None:
        pass

    # async def __call__(self, message: types.Message) -> bool:
    #     if message.from_user.id in config.tg_bot.id_admins:
    #         return True
    #     else:
    #         await message.answer(text="Нет прав")

    async def __call__(self, message_or_callback) -> bool:
        if isinstance(message_or_callback, types.Message):
            message = message_or_callback
            if message.from_user.id in config.tg_bot.id_admins:
                return True
            # else:
            #     await message.answer(text="Нет прав")
        elif isinstance(message_or_callback, types.CallbackQuery):
            callback_query = message_or_callback
            if callback_query.from_user.id in config.tg_bot.id_admins:
                return True
            # else:
            #     await callback_query.message.answer(text="Нет прав")