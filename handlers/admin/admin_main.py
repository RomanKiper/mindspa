from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config_data.config import Config, load_config
from filters.chat_types import ChatTypeFilter
from filters.is_admin import IsAdminMsg
from keyboards.inline.inline import get_callback_btns, get_inlineMix_btns
from lexicon.lexicon import LEXICON_btn_main_admin_menu, LEXICON_ADMIN, LEXICON_btn_BACK_main_admin_menu

from aiogram.filters import Command, or_f
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
config: Config = load_config()

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdminMsg())
admin_router.callback_query.filter(IsAdminMsg())


@admin_router.message(Command("admin"), F.text | F.command)
@admin_router.message(F.text.lower().in_({'admin', 'administrator', "админ", "администратор"}))
async def admin_handler_message(message:Message):
    await message.answer(text=LEXICON_ADMIN["/admin+panel"],
                         reply_markup=get_callback_btns(btns=LEXICON_btn_main_admin_menu, sizes=(2,)))

@admin_router.callback_query(F.data == "admin_menu")
async def admin_handler_caccback(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_ADMIN["/admin+panel"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_main_admin_menu,sizes=(2,)))


@admin_router.callback_query(F.data == "instruction_admin")
async def get_admin_instruction(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_ADMIN["/instruction_description"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_BACK_main_admin_menu))
