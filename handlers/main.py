from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import (orm_add_request_course_information, orm_add_code_missing_information,
                                orm_add_user, orm_add_information_cannotlogin, orm_add_information_whereentercode,
                                orm_add_info_badcode, orm_add_info_noquestion)
from config_data.config import Config, load_config

from filters.chat_types import ChatTypeFilter
from keyboards.inline.inline import get_callback_btns, get_inlineMix_btns
from lexicon.lexicon import (LEXICON_btn_questions, LEXICON_RU, LEXICON_btn_answer_questions,
                             LEXICON_btn_helh_with_code, LEXICON_btn_code_do_not_work,
                             LEXICON_btn_model_phone, LEXICON_btn_back_to_questions, LEXICON_btn_logging_instruction,
                             LEXICON_btn_no_my_question, LEXICON_btn_back_and_video_android,
                             LEXICON_btn_back_and_video_iphone)
from lexicon.lexicon import PDF_FILE_ANDR_INTR, PDF_FILE_IPHONE_INTR, VIDEO_FILE_ANDR_INTR, VIDEO_FILE_IPHONE_INTR

from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

config: Config = load_config()

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(F.text.lower().in_({'вопросы', 'вопрос', "questions", "старт", "start", "начать"}))
@user_private_router.message(CommandStart())
@user_private_router.message(Command('questions'))
@user_private_router.callback_query(F.data == 'main_list_questions')
async def start_cmd(message_or_callback: types.Union[types.Message, CallbackQuery], session: AsyncSession):
    if isinstance(message_or_callback, types.Message):
        message = message_or_callback
        await orm_add_user(session,
                           user_id=message.from_user.id,
                           username=message.from_user.username,
                           first_name=message.from_user.first_name,
                           last_name=message.from_user.last_name,
                           )
        await message.answer(text=LEXICON_RU["/question_list"],
                             reply_markup=get_callback_btns(btns=LEXICON_btn_questions, sizes=(1,)),
                             disable_web_page_preview=True)
        # await message.delete()

    elif isinstance(message_or_callback, types.CallbackQuery):
        callback = message_or_callback
        await callback.message.answer(text=LEXICON_RU["/question_list"],
                                      reply_markup=get_callback_btns(btns=LEXICON_btn_questions, sizes=(1,)),
                                      disable_web_page_preview=True)
        # await callback.message.delete()


@user_private_router.callback_query(F.data == 'do_not_have_code')
async def get_help_with_code(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/help_with_code"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_helh_with_code, sizes=(1,)))
    # await callback.message.delete()


@user_private_router.callback_query(F.data == 'help_with_course')
async def get_help_with_questions(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/help_with_course"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_answer_questions, sizes=(1,)))
    # await callback.message.delete()


###########################################FSM for question form#########################

class AddRequestCourse(StatesGroup):
    # Шаги состояний
    question1 = State()
    question2 = State()
    question3 = State()
    contact_information = State()

    # product_for_change = None

    texts = {
        'AddRequestCourse:question1': 'Ответь на вопрос №1 заново. "Проблема, которую я хочу решить - ..."',
        'AddRequestCourse:question2': 'Ответь на вопрос №2 заново. "Как проявляется твоя проблема в мыслях, чувствах, ощущениях, поведении?"',
        'AddRequestCourse:question3': 'Ответь на вопрос №3 заново. "Результат, которого я хочу достичь — ..."',
        'AddRequestCourse:contact_information': 'Этот стейт последний, поэтому...',
    }

# Вернутся на шаг назад (на прошлое состояние)
@user_private_router.message(StateFilter("*"), Command("назад"))
@user_private_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddRequestCourse.question1:
        await message.answer(
            'Предидущего шага нет. Напиши ОТМЕНА или ответь на первый вопрос - "Проблема, которую я хочу решить - ..."'
        )
        return
    previous = None
    for step in AddRequestCourse.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, ты вернулся к прошлому шагу.\n{AddRequestCourse.texts[previous.state]}"
            )
            return
        previous = step


# Становимся в состояние ожидания ввода ответ на вопрос №1
@user_private_router.callback_query(StateFilter(None), F.data == 'first_question_form')
async def question_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("<b>Ответь на первый вопрос.</b>\n<i>Проблема, которую я хочу решить - ...</i>")
    # await callback.message.delete()
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
                "Ответ на вопос должен быть более развернутым🤔\nВведи ответ на вопрос заново."
            )
        else:
            await state.update_data(question1=message.text)
            await message.answer("<b>Ответь на второй вопрос.</b>\n<i>Как проявляется твоя проблема в мыслях, чувствах, ощущениях, поведении?</i>")
            await state.set_state(AddRequestCourse.question2)


# Хендлер для отлова некорректных вводов для состояния question1
@user_private_router.message(AddRequestCourse.question1)
async def add_question1_2(message: types.Message, state: FSMContext):
    await message.answer("Ты ввел не допустимые данные, введи текст ответа заново!")


# Ловим данные для состояние question2 и потом меняем состояние на question3
@user_private_router.message(AddRequestCourse.question2, F.text)
async def add_question2(message: types.Message, state: FSMContext):
    if message.text:
        if len(message.text) < 5:
            await message.answer(
                "Ответ на вопос должен быть более развернутым🤔\nВведи ответ на вопрос заново."
            )
        else:
            await state.update_data(question2=message.text)
            await message.answer("<b>Ответь на третий вопрос.</b>\n<i>Результат, которого я хочу достичь — ...</i>")
            await state.set_state(AddRequestCourse.question3)


# Хендлер для отлова некорректных вводов для состояния question2
@user_private_router.message(AddRequestCourse.question2)
async def add_question2_2(message: types.Message, state: FSMContext):
    await message.answer("Ты ввел не допустимые данные, введи текст ответа заново!")


# Ловим данные для состояние question3
@user_private_router.message(AddRequestCourse.question3, F.text)
async def add_question3(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if message.text:
        if len(message.text) < 5:
            await message.answer(
                "Ответ на вопос должен быть более развернутым🤔\nВведи ответ на вопрос заново."
            )
        else:
            await state.update_data(question3=message.text)
            data = await state.get_data()

            user_id = message.from_user.id
            full_name = message.from_user.full_name
            username_ = message.from_user.username
            user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
            user_link2 = f"<a href='tg://user?id={user_id}'>Ссылка на пользователя</a>"

            # Форматирование данных для отправки администратору
            formatted_data = (
                f"<b>Новый запрос на курс:</b>\n"
                f"✅Сообщение от:\n"
                f"username пользователя:\n@{username_}\n"
                f"{user_link2}:\n{user_link}\n"
                f"✅1.Проблема, которую я хочу решить — \n{data.get('question1')}\n"
                f"✅2.Как проявляется твоя проблема в мыслях, чувствах, ощущениях, поведении?\n{data.get('question2')}\n"
                f"✅3.Результат, которого я хочу достичь — ...\n{data.get('question3')}\n"
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
                    "Спасибо за твои ответы.\nНаш психолог даст тебе обратную связь"
                    " в течение несколько часов, в редких случаях в срок до 24 часов.",
                    reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))
                await state.clear()

            except Exception as e:
                await message.answer(
                    f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет", sizes=(2,))
                await state.clear()


# Хендлер для отлова некорректных вводов для состояния question3
@user_private_router.message(AddRequestCourse.question3)
async def add_question3(message: types.Message, state: FSMContext):
    await message.answer("Ты ввел не допустимые данные, введи текст ответа заново!")


########################################  end FSM for question form###################################################################


#####################################FSM for code missing form ######################################################

class AddSendMail(StatesGroup):
    # Шаги состояний
    sending_mail = State()


# cтановимся в состояние ожидания ответа sending_mail
@user_private_router.callback_query(StateFilter(None), F.data == 'send_mail_adress')
async def question_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("<b>Пришли электронный адрес, который был указан при покупке.</b>")
    # await callback.message.delete()
    await state.set_state(AddSendMail.sending_mail)


# Ловим данные для состояние sending_mail
@user_private_router.message(AddSendMail.sending_mail, F.text)
async def add_sending_mail_information(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if message.text:
        if len(message.text) < 3:
            await message.answer(
                "Думаю этого не достаточно, чтобы связаться с тобой. Напиши еще раз!"
            )
        else:
            await state.update_data(sending_mail=message.text)
            data = await state.get_data()

            user_id = message.from_user.id
            full_name = message.from_user.full_name
            username_ = message.from_user.username
            user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
            user_link2 = f"<a href='tg://user?id={user_id}'>Ссылка на пользователя</a>"

            # Форматирование данных для отправки администратору
            formatted_data = (
                f"<b>Новый запрос.</b>\n"
                f"Не пришел код.\n"
                f"✅Сообщение от:\n"
                f"username пользователя:\n@{username_}\n"
                f"{user_link2}:\n{user_link}\n"
                f"✅Адрес электронной почты, который был указан при покупке:\n{data.get('sending_mail')}\n"
            )

            # Отправка сообщения администратору
            admin_id = config.tg_bot.id_chat_admin
            await bot.send_message(chat_id=admin_id, text=formatted_data)

            try:
                await orm_add_code_missing_information(session=session,
                                                       data=data,
                                                       user_id=message.from_user.id,
                                                       username=message.from_user.username,
                                                       first_name=message.from_user.first_name,
                                                       last_name=message.from_user.last_name)
                await message.answer(text=LEXICON_RU['/answer_about_code'],
                                     reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))
                await state.clear()
            except Exception as e:
                await message.answer(
                    f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет", sizes=(2,))
                await state.clear()


# Хендлер для отлова некорректных вводов для состояния sending_mail
@user_private_router.message(AddSendMail.sending_mail)
async def add_sending_mail_information_2(message: types.Message, state: FSMContext):
    await message.answer("Ты ввел не допустимые данные, введи текст ответа заново!")


@user_private_router.callback_query(F.data == 'question_is_solved')
async def question_form_finish_answer(callback: types.CallbackQuery):
    await callback.message.answer("<b>Спасибо!</b>\n"
                                  "Команда Mindspa рада помочь тебе.",
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))
    # await callback.message.delete()


##################################################bad code###########################

@user_private_router.callback_query(F.data == 'bad_code')
async def get_answer_bad_code(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/bad_code"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_code_do_not_work, sizes=(1,)))
    # await callback.message.delete()


@user_private_router.callback_query(F.data == 'problem_is_solved')
async def get_answer_problem_solved(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/bad_code_problem_solved"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))
    # await callback.message.delete()


@user_private_router.callback_query(F.data == 'problem_is_not_solved')
async def get_answer_problem_not_solved(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    await orm_add_info_badcode(session=session,
                               user_id=callback.from_user.id,
                               username=callback.from_user.username,
                               first_name=callback.from_user.first_name,
                               last_name=callback.from_user.last_name)
    await callback.message.answer(text=LEXICON_RU["/bad_code_problem_not_solved"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))
    user_id = callback.from_user.id
    full_name = callback.from_user.full_name
    username_ = callback.from_user.username
    user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
    user_link2 = f"<a href='tg://user?id={user_id}'>Ссылка на пользователя</a>"

    # Форматирование данных для отправки администратору
    formatted_data = (
        f"<b>Новый запрос.</b>\n"
        f"Мне пришел код, но он не работает.\n"
        f"✅Сообщение от:\n"
        f"username пользователя:\n@{username_}\n"
        f"{user_link2}:\n{user_link}\n"
    )

    # Отправка сообщения администратору
    admin_id = config.tg_bot.id_chat_admin
    await bot.send_message(chat_id=admin_id, text=formatted_data)
    # await callback.message.delete()


################################################## end bad code###########################

################################################## entering code instruction ##############

@user_private_router.callback_query(F.data == 'do_not_now_how_to_enter_code')
async def get_instruction_code(callback: types.CallbackQuery, session: AsyncSession):
    await orm_add_information_whereentercode(session=session,
                                           user_id=callback.from_user.id,
                                           username=callback.from_user.username,
                                           first_name=callback.from_user.first_name,
                                           last_name=callback.from_user.last_name)
    await callback.message.answer(text=LEXICON_RU["/instruction_entering_code"],
                                  reply_markup=get_inlineMix_btns(btns=LEXICON_btn_model_phone, sizes=(2,)),
                                  disable_web_page_preview=True)
    # await callback.message.delete()


@user_private_router.callback_query(F.data == 'android_phone')
async def send_pdf_android(calback: CallbackQuery):
    try:
        # Отправка PDF-документа по его ID
        await calback.message.answer_document(document=PDF_FILE_ANDR_INTR,
                                              caption=LEXICON_RU['/instruction_android'],
                                              reply_markup=get_callback_btns(btns=LEXICON_btn_back_and_video_android,
                                                                             sizes=(1,)))

    except Exception as e:
        await calback.message.answer(f"Произошла ошибка при отправке документа: {str(e)}")


@user_private_router.callback_query(F.data == 'video_android')
async def send_pdf_android(calback: CallbackQuery):
    try:
        # Отправка PDF-документа по его ID
        await calback.message.answer_video(video=VIDEO_FILE_ANDR_INTR,
                                           caption="Видеоинструкция.",
                                           reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))

    except Exception as e:
        await calback.message.answer(f"Произошла ошибка при отправке документа: {str(e)}")


@user_private_router.callback_query(F.data == 'iphone_phone')
async def send_pdf_iphone(calback: CallbackQuery):
    try:
        # Отправка PDF-документа по его ID
        await calback.message.answer_document(document=PDF_FILE_IPHONE_INTR,
                                              caption=LEXICON_RU['/instruction_iphone'],
                                              reply_markup=get_callback_btns(btns=LEXICON_btn_back_and_video_iphone,
                                                                             sizes=(1,)))

    except Exception as e:
        await calback.message.answer(f"Произошла ошибка при отправке документа: {str(e)}")


@user_private_router.callback_query(F.data == 'video_iphone')
async def send_video_iphone(calback: CallbackQuery):
    try:
        # Отправка PDF-документа по его ID
        await calback.message.answer_video(video=VIDEO_FILE_IPHONE_INTR,
                                           caption='Видеоинструкция.',
                                           reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))

    except Exception as e:
        await calback.message.answer(f"Произошла ошибка при отправке документа: {str(e)}")


################################################## end  entering code instruction ##############################


################################################## I can't log into my account###########################

@user_private_router.callback_query(F.data == 'can_not_enter_account')
async def get_information_entering(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/instruction_entering_accaunt"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_logging_instruction, sizes=(1,)))
    # await callback.message.delete()


class AddLogAccaunt(StatesGroup):
    # Шаги состояний
    log_sending_mail = State()


# cтановимся в состояние ожидания ответа sending_mail
@user_private_router.callback_query(StateFilter(None), F.data == 'log_send_mail_to_admin')
async def log_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("<b>Пожалуйста, пришли электронный адрес, который был указан при регистрации.</b>")
    # await callback.message.delete()
    await state.set_state(AddLogAccaunt.log_sending_mail)


# Ловим данные для состояние sending_mail
@user_private_router.message(AddLogAccaunt.log_sending_mail, F.text)
async def add_sending_mail_information_log(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if message.text:
        if len(message.text) < 3:
            await message.answer(
                "Думаю этого не достаточно, чтобы связаться с тобой. Напиши еще раз!"
            )
        else:
            await state.update_data(log_sending_mail=message.text)
            data = await state.get_data()

            user_id = message.from_user.id
            full_name = message.from_user.full_name
            username_ = message.from_user.username
            user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
            user_link2 = f"<a href='tg://user?id={user_id}'>Ссылка на пользователя</a>"

            # Форматирование данных для отправки администратору
            formatted_data = (
                f"<b>Новое сообщение.</b>\n"
                f"Не могу войти в аккаунт.\n"
                f"✅Сообщение от:\n"
                f"username пользователя:\n@{username_}\n"
                f"{user_link2}:\n{user_link}\n"
                f"✅Адрес электронной почты, который был указан при регистрации:\n{data.get('log_sending_mail')}\n"
            )

            # Отправка сообщения администратору
            admin_id = config.tg_bot.id_chat_admin
            await bot.send_message(chat_id=admin_id, text=formatted_data)

            try:
                await orm_add_information_cannotlogin(session=session,
                                                       data=data,
                                                       user_id=message.from_user.id,
                                                       username=message.from_user.username,
                                                       first_name=message.from_user.first_name,
                                                       last_name=message.from_user.last_name)
                await message.answer(text=LEXICON_RU['/log_code_answer'],
                                     reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))

                await state.clear()
            except Exception as e:
                await message.answer(
                    f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет", sizes=(2,))
                await state.clear()


# Хендлер для отлова некорректных вводов для состояния log_sending_mail
@user_private_router.message(AddLogAccaunt.log_sending_mail)
async def add_sending_mail_information_log_2(message: types.Message, state: FSMContext):
    await message.answer("Ты ввел не допустимые данные, введи текст ответа заново!")


@user_private_router.callback_query(F.data == 'log_problem_is_solved')
async def question_form_finish_answer(callback: types.CallbackQuery):
    await callback.message.answer("<b>Спасибо!</b>\n"
                                  "Команда Mindspa рада помочь тебе.",
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))
    # await callback.message.delete()


################################################## end I can't log into my account###########################

################################################## My question is not in list ###########################

@user_private_router.callback_query(F.data == 'no_my_question')
async def get_no_my_question(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/no_my_question"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_no_my_question, sizes=(1,)))
    # await callback.message.delete()


class AddNewQuestion(StatesGroup):
    # Шаги состояний
    new_question = State()


# cтановимся в состояние ожидания ответа new_question
@user_private_router.callback_query(StateFilter(None), F.data == 'write_new_question')
async def get_form_new_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("<b>Напиши какой у тебя вопрос.</b>")
    # await callback.message.delete()
    await state.set_state(AddNewQuestion.new_question)


# Ловим данные для состояние new_question
@user_private_router.message(AddNewQuestion.new_question, F.text)
async def add_new_question_information(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if message.text:
        if len(message.text) < 4:
            await message.answer(
                "Напиши больше информации!"
            )
        else:
            await state.update_data(new_question=message.text)
            data = await state.get_data()

            user_id = message.from_user.id
            full_name = message.from_user.full_name
            username_ = message.from_user.username
            user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
            user_link2 = f"<a href='tg://user?id={user_id}'>Ссылка на пользователя</a>"

            # Форматирование данных для отправки администратору
            formatted_data = (
                f"<b>Новое сообщение.</b>\n"
                f"В списке нет моего вопроса.\n"
                f"✅Сообщение от:\n"
                f"username пользователя:\n@{username_}\n"
                f"{user_link2}:\n{user_link}\n"
                f"✅Текс сообщения от пользователя:\n{data.get('new_question')}\n"
            )

            # Отправка сообщения администратору
            admin_id = config.tg_bot.id_chat_admin
            await bot.send_message(chat_id=admin_id, text=formatted_data)
            try:
                await orm_add_info_noquestion(session=session,
                                                       data=data,
                                                       user_id=message.from_user.id,
                                                       username=message.from_user.username,
                                                       first_name=message.from_user.first_name,
                                                       last_name=message.from_user.last_name)
                await message.answer(text=LEXICON_RU['/finish_answer'],
                                     reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_questions))
                await state.clear()
            except Exception as e:
                await message.answer(
                    f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет", sizes=(2,))
                await state.clear()


# Хендлер для отлова некорректных вводов для состояния new_question
@user_private_router.message(AddNewQuestion.new_question)
async def add_new_question_information_2(message: types.Message, state: FSMContext):
    await message.answer("Ты ввел не допустимые данные, введи текст ответа заново!")


############################################################################
# @user_private_router.message()
# async def send_echo(message: Message):
#     try:
#         if message.photo:
#             await message.send_copy(chat_id=message.chat.id)
#             photo_id = message.photo[0].file_id
#             await message.answer(f"ID фотографии: {photo_id}")
#         elif message.video:
#             await message.send_copy(chat_id=message.chat.id)
#             video_id = message.video.file_id
#             await message.answer(f"ID видео: {video_id}")
#         elif message.document:
#             await message.send_copy(chat_id=message.chat.id)
#             document_id = message.document.file_id
#             await message.answer(f"ID документа: {document_id}")
#     except TypeError:
#         await message.reply(text=LEXICON_RU['no_echo'])
