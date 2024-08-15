from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_request_course_information
from config_data.config import Config, load_config

from filters.chat_types import ChatTypeFilter
from keyboards.inline.inline import get_callback_btns
from lexicon.lexicon import (LEXICON_btn_questions, LEXICON_RU, LEXICON_btn_answer_questions,
                             LEXICON_btn_helh_with_code,
                             LEXICON_btn_code_do_not_work)

from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

config: Config = load_config()

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


# user_private_router.callback_query.filter(ChatTypeFilter(['private']))


@user_private_router.message(F.text.lower().in_({'вопросы', 'вопрос', "questions"}))
@user_private_router.message(CommandStart())
@user_private_router.message(Command('questions'))
@user_private_router.callback_query(F.data == 'main_list_questions')
async def start_cmd(message_or_callback: types.Union[types.Message, CallbackQuery], session: AsyncSession):
    if isinstance(message_or_callback, types.Message):
        message = message_or_callback
        await message.answer(text=LEXICON_RU["/question_list"],
                             reply_markup=get_callback_btns(btns=LEXICON_btn_questions, sizes=(1,)))
        await message.delete()

    elif isinstance(message_or_callback, types.CallbackQuery):
        callback = message_or_callback
        await callback.message.answer(text=LEXICON_RU["/question_list"],
                                      reply_markup=get_callback_btns(btns=LEXICON_btn_questions, sizes=(1,)))
        await callback.message.delete()


@user_private_router.callback_query(F.data == 'do_not_have_code')
async def get_help_with_code(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/help_with_code"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_helh_with_code, sizes=(1,)))
    await callback.message.delete()


@user_private_router.callback_query(F.data == 'help_with_course')
async def get_help_with_questions(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/help_with_course"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_answer_questions, sizes=(1,)))
    await callback.message.delete()


###########################################FSM for question form#########################

class AddRequestCourse(StatesGroup):
    # Шаги состояний
    question1 = State()
    question2 = State()
    question3 = State()
    contact_information = State()

    # product_for_change = None

    texts = {
        'AddRequestCourse:question1': 'Ответьте на вопрос №1 заново. "Проблема, которую я хочу решить - ..."',
        'AddRequestCourse:question2': 'Ответьте на вопрос №2 заново. "Моя проблема выражается в...."',
        'AddRequestCourse:question3': 'Ответьте на вопрос №3 заново. "Результат, которого я хочу достичь — ..."',
        'AddRequestCourse:contact_information': 'Этот стейт последний, поэтому...',
    }


# Вернутся на шаг назад (на прошлое состояние)
@user_private_router.message(StateFilter("*"), Command("назад"))
@user_private_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddRequestCourse.question1:
        await message.answer(
            'Предидущего шага нет. Напишите ОТМЕНА или ответьте на вопрос №1 - "Проблема, которую я хочу решить - ..."'
        )
        return
    previous = None
    for step in AddRequestCourse.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу.\n{AddRequestCourse.texts[previous.state]}"
            )
            return
        previous = step


# Становимся в состояние ожидания ввода ответ на вопрос №1
@user_private_router.callback_query(StateFilter(None), F.data == 'first_question_form')
async def question_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("<b>Ответьте на первый вопрос.</b>\n<i>Проблема, которую я хочу решить - ...</i>")
    await callback.message.delete()
    await state.set_state(AddRequestCourse.question1)


# Хендлер отмены и сброса состояния должен быть всегда именно здесь,
# после того как только встали в состояние номер 1 (элементарная очередность фильтров)
@user_private_router.message(StateFilter("*"), Command("отмена"))
@user_private_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text=LEXICON_RU["/help_with_course"],
                         reply_markup=get_callback_btns(btns=LEXICON_btn_answer_questions, sizes=(1,)))


# Ловим данные для состояние question1 и потом меняем состояние на question2
@user_private_router.message(AddRequestCourse.question1, F.text)
async def add_question1(message: types.Message, state: FSMContext):
    if message.text:
        if len(message.text) < 5:
            await message.answer(
                "Ответ на вопос должен быть более развернутым🤔\nВведите ответ на вопрос заново."
            )
        else:
            await state.update_data(question1=message.text)
            await message.answer("<b>Ответьте на второй вопрос.</b>\n<i>Моя проблема выражается в....</i>")
            await state.set_state(AddRequestCourse.question2)


# Хендлер для отлова некорректных вводов для состояния question1
@user_private_router.message(AddRequestCourse.question1)
async def add_question1_2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст ответа заново!")


# Ловим данные для состояние question2 и потом меняем состояние на question3
@user_private_router.message(AddRequestCourse.question2, F.text)
async def add_question2(message: types.Message, state: FSMContext):
    if message.text:
        if len(message.text) < 5:
            await message.answer(
                "Ответ на вопос должен быть более развернутым🤔\nВведите ответ на вопрос заново."
            )
        else:
            await state.update_data(question2=message.text)
            await message.answer("<b>Ответьте на третий вопрос.</b>\n<i>Результат, которого я хочу достичь — ...</i>")
            await state.set_state(AddRequestCourse.question3)


# Хендлер для отлова некорректных вводов для состояния question2
@user_private_router.message(AddRequestCourse.question2)
async def add_question2_2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст ответа заново!")


# Ловим данные для состояние question3 и потом меняем состояние на contact_information
@user_private_router.message(AddRequestCourse.question3, F.text)
async def add_question3(message: types.Message, state: FSMContext):
    if message.text:
        if len(message.text) < 5:
            await message.answer(
                "Ответ на вопос должен быть более развернутым🤔\nВведите ответ на вопрос заново."
            )
        else:
            await state.update_data(question3=message.text)
            await message.answer("<b>Напишите как вам удобно, чтобы с вами связались?</b>")
            await state.set_state(AddRequestCourse.contact_information)


# Хендлер для отлова некорректных вводов для состояния question3
@user_private_router.message(AddRequestCourse.question3)
async def add_question3_2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст ответа заново!")


# Ловим данные для состояние contact_information
@user_private_router.message(AddRequestCourse.contact_information, F.text)
async def add_contact_information3(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if message.text:
        if len(message.text) < 3:
            await message.answer(
                "Думаю этого не достаточно, чтобы связаться с вами. Напишите еще раз!"
            )
        else:
            await state.update_data(contact_information=message.text)
            data = await state.get_data()

            user_id = message.from_user.id
            full_name = message.from_user.full_name
            username_ = message.from_user.username
            user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"

            # Форматирование данных для отправки администратору
            formatted_data = (
                f"<b>Новый запрос на курс:</b>\n"
                f"✅Сообщение от:\n"
                f"username пользователя:\n@{username_}\n"
                f"Ссылка на пользователя:\n{user_link}\n"
                f"✅1.Проблема, которую я хочу решить — ...\n{data.get('question1')}\n"
                f"✅2.Моя проблема выражается в....\n{data.get('question2')}\n"
                f"✅3.Результат, которого я хочу достичь — ...\n{data.get('question3')}\n"
                f"✅Удобный для меня способ связи:\n{data.get('contact_information')}\n"
            )

            # Отправка сообщения администратору
            admin_id = config.tg_bot.id_chat_admin
            await bot.send_message(chat_id=admin_id, text=formatted_data)

            try:
                await orm_add_request_course_information(session=session,
                                                         data=data,
                                                         user_id=message.from_user.id,
                                                         username=message.from_user.username,
                                                         first_name=message.from_user.first_name,
                                                         last_name=message.from_user.last_name)
                await message.answer(
                    "Спасибо за ваши ответы.\nНаш психолог даст тебе обратную связь в течение несколько часов, в редких случаях в срок до 24 часов.")
                await state.clear()

            except Exception as e:
                await message.answer(
                    f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет", sizes=(2,))
                await state.clear()


# Хендлер для отлова некорректных вводов для состояния contact_information
@user_private_router.message(AddRequestCourse.contact_information)
async def add_contact_information_2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст ответа заново!")


########################################  end FSM for question form###################################################################


#####################################FSM for code form ######################################################

class AddSendMail(StatesGroup):
    # Шаги состояний
    sending_mail = State()


# cтановимся в состояние ожидания ответа sending_mail
@user_private_router.callback_query(StateFilter(None), F.data == 'send_mail_adress')
async def question_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("<b>Пришлите электронный адрес, который был указан при покупке.</b>")
    await callback.message.delete()
    await state.set_state(AddSendMail.sending_mail)


# Ловим данные для состояние sending_mail
@user_private_router.message(AddSendMail.sending_mail, F.text)
async def add_sending_mail_information(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if message.text:
        if len(message.text) < 3:
            await message.answer(
                "Думаю этого не достаточно, чтобы связаться с вами. Напишите еще раз!"
            )
        else:
            await state.update_data(sending_mail=message.text)
            data = await state.get_data()

            user_id = message.from_user.id
            full_name = message.from_user.full_name
            username_ = message.from_user.username
            user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"

            # Форматирование данных для отправки администратору
            formatted_data = (
                f"<b>Новый запрос на получение кода:</b>\n"
                f"✅Сообщение от:\n"
                f"username пользователя:\n@{username_}\n"
                f"Ссылка на пользователя:\n{user_link}\n"
                f"✅Адрес электронной почты, который был указан при покупке:\n{data.get('sending_mail')}\n"
            )

            # Отправка сообщения администратору
            admin_id = config.tg_bot.id_chat_admin
            await bot.send_message(chat_id=admin_id, text=formatted_data)

            try:
                await message.answer(
                    "Спасибо!\nТвой запрос и адрес переданы в службу технической поддержки. "
                    "Доступ поступит на указанную тобой электронную почту. "
                    "Обычно это занимает несколько часов, в редких случаях — до 24 часов.")
                await state.clear()
            except Exception as e:
                await message.answer(
                    f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет", sizes=(2,))
                await state.clear()


# Хендлер для отлова некорректных вводов для состояния question3
@user_private_router.message(AddSendMail.sending_mail)
async def add_sending_mail_information_2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст ответа заново!")


@user_private_router.callback_query(F.data == 'question_is_solved')
async def question_form_finish_answer(callback: types.CallbackQuery):
    await callback.message.answer("Спасибо!\n"
                                  "Команда Mindspa рада помочь вам.")
    await callback.message.delete()


##################################################bad code###########################

@user_private_router.callback_query(F.data == 'bad_code')
async def get_answer_bad_code(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/bad_code"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_code_do_not_work, sizes=(1,)))
    await callback.message.delete()


@user_private_router.callback_query(F.data == 'problem_is_solved')
async def get_answer_problem_solved(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/bad_code_problem_solved"], )
    await callback.message.delete()


@user_private_router.callback_query(F.data == 'problem_is_not_solved')
async def get_answer_problem_not_solved(callback: types.CallbackQuery, bot: Bot):
    await callback.message.answer(text=LEXICON_RU["/bad_code_problem_not_solved"], )

    user_id = callback.from_user.id
    full_name = callback.from_user.full_name
    username_ = callback.from_user.username
    user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"

    # Форматирование данных для отправки администратору
    formatted_data = (
        f"<b>Новый запрос.</b>\n"
        f"Мне пришел код, но он не работает.\n"
        f"✅Сообщение от:\n"
        f"username пользователя:\n@{username_}\n"
        f"Ссылка на пользователя:\n{user_link}\n"
    )

    # Отправка сообщения администратору
    admin_id = config.tg_bot.id_chat_admin
    await bot.send_message(chat_id=admin_id, text=formatted_data)
    await callback.message.delete()

################################################## end bad code###########################

##################################################entering code instruction ###########################