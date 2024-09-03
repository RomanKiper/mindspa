from aiogram import types, Router, F, Bot
import pandas as pd

from aiogram.types import FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config_data.config import Config, load_config
from filters.chat_types import ChatTypeFilter
from filters.is_admin import IsAdminMsg
from keyboards.inline.inline import get_callback_btns, get_inlineMix_btns
from lexicon.lexicon import LEXICON_btn_main_admin_menu, LEXICON_ADMIN, LEXICON_btn_BACK_main_admin_menu
from database.orm_query import orm_get_users
from database.models import User, CourseRequest
from aiogram.filters import Command, or_f
from dotenv import find_dotenv, load_dotenv

from sqlalchemy.future import select

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


@admin_router.callback_query(F.data == "users_all_list")
async def get_users_list(callback: CallbackQuery, session: AsyncSession):
    # Получение всех пользователей из базы данных
    result = await session.execute(select(User))
    users = result.scalars().all()

    # Создание списка словарей, где ключи соответствуют столбцам
    data = [
        {
            "ID": user.id,
            "User ID": user.user_id,
            "ИМЯ/First Name": user.first_name,
            "ФАМИЛИЯ/Last Name": user.last_name,
            "ЛОГИН/Username": user.username,
            "НОМЕР ТЕЛ./Phone": user.phone
        }
        for user in users
    ]

    # Создание DataFrame из списка словарей
    df = pd.DataFrame(data)
    print(df)

    # Указание имени файла
    file_name = "users_data.xlsx"

    # Сохранение DataFrame в Excel-файл
    df.to_excel(file_name, index=False)

    # Создание InputFile с использованием пути к файлу
    input_file = FSInputFile(file_name)

    # Отправка файла
    await callback.message.answer_document(input_file)


@admin_router.callback_query(F.data == "report_users")
async def get_admin_report(callback: CallbackQuery, session: AsyncSession):
    # Получение всех пользователей из базы данных
    result_help_with_coure = await session.execute(select(CourseRequest))
    requests = result_help_with_coure.scalars().all()

    # Создание списка словарей, где ключи соответствуют столбцам
    data = [
        {
            "ID": req.id,
            "User ID": req.user_id,
            "ИМЯ/First Name": req.first_name,
            "ФАМИЛИЯ/Last Name": req.last_name,
            "ЛОГИН/Username": req.username,
            "question1": req.question1,
            "question2": req.question2,
            "question3": req.question3,
        }
        for req in requests
    ]

    # Создание DataFrame из списка словарей
    df = pd.DataFrame(data)
    print(df)

    # Указание имени файла
    file_name = "report.xlsx"

    # Сохранение DataFrame в Excel-файл
    df.to_excel(file_name, index=False)

    # Создание InputFile с использованием пути к файлу
    input_file = FSInputFile(file_name)

    # Отправка файла
    await callback.message.answer_document(input_file)