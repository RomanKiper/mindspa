from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_request_course_information
from config_data.config import Config, load_config

from filters.chat_types import ChatTypeFilter
from keyboards.inline.inline import get_callback_btns
from lexicon.lexicon import LEXICON_btn_questions, LEXICON_RU, LEXICON_btn_answer_questions

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


@user_private_router.callback_query(F.data == 'help_with_course')
async def get_help_with_questions(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU["/help_with_course"],
                                  reply_markup=get_callback_btns(btns=LEXICON_btn_answer_questions, sizes=(1,)))
    await callback.message.delete()


###########################################

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


#
# @admin_router.callback_query(F.data == 'products_list')
# async def admin_features(callback: types.CallbackQuery, session: AsyncSession):
#     categories = await orm_get_categories(session)
#     btns = {category.name: f'category_{category.id}' for category in categories}
#     await callback.message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns))
#
#
# @admin_router.callback_query(F.data.startswith('category_'))
# async def starring_at_product(callback: types.CallbackQuery, session: AsyncSession):
#     category_id = callback.data.split('_')[-1]
#     user_id = callback.from_user.id
#     print(user_id)
#     for product in await orm_get_products(session, int(category_id), int(user_id)):
#         await callback.message.answer_photo(
#             product.image,
#             caption=f"<strong>{product.name}\
#                     </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
#             reply_markup=get_callback_btns(
#                 btns={
#                     "Удалить": f"delete_{product.id}",
#                     "Изменить": f"change_{product.id}",
#                 },
#                 sizes=(2,)
#             ),
#         )
#     await callback.answer()
#     await callback.message.answer("ОК, вот список товаров ⏫")
#
#
# @admin_router.callback_query(F.data.startswith("delete_"))
# async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
#     product_id = callback.data.split("_")[-1]
#     await orm_delete_product(session, int(product_id))
#
#     await callback.answer("Товар удален")
#     await callback.message.answer("Товар удален!")
#
# # FSM:
#
# @admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
# async def change_product_callback(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
#     product_id = callback.data.split("_")[-1]
#     product_for_change = await orm_get_product(session, int(product_id))
#     AddProduct.product_for_change = product_for_change
#     await callback.answer()
#     await callback.message.answer(
#         "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AddProduct.name)
#
#
# Становимся в состояние ожидания ввода ответ на вопрос №1
@user_private_router.callback_query(StateFilter(None), F.data == 'first_question_form')
async def question_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Ответьте на первыйй вопрос. Проблема, которую я хочу решить - ...")
    await callback.message.delete()
    await state.set_state(AddRequestCourse.question1)


# Хендлер отмены и сброса состояния должен быть всегда именно хдесь,
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
            await message.answer("Ответьте на второй вопрос.\nМоя проблема выражается в....")
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
            await message.answer("Ответьте на третий вопрос.\nРезультат, которого я хочу достичь — ...")
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
            await message.answer("Напишите как вам удобно, чтобы с вами связались?")
            await state.set_state(AddRequestCourse.contact_information)


# Хендлер для отлова некорректных вводов для состояния question3
@user_private_router.message(AddRequestCourse.question3)
async def add_question3_2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст ответа заново!")


# Ловим данные для состояние question3 и потом меняем состояние на contact_information
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

            username_ = message.from_user.username

            # Форматирование данных для отправки администратору
            formatted_data = (
                f"Новый запрос на курс:\n"
                f"✅username пользователя:\n@{username_}\n"
                f"✅1.Проблема, которую я хочу решить — ...\n{data.get('question1')}\n"
                f"✅2.Моя проблема выражается в....\n{data.get('question2')}\n"
                f"✅3.Результат, которого я хочу достичь — ...\n{data.get('question3')}\n"
                f"✅Удобный для меня способ связи:\n{data.get('contact_information')}\n"
                # Добавьте другие поля из data, если нужно
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
                await message.answer("Спасибо за ваши ответы. Мы с вами свжемся в ближайшее время.")
                await state.clear()

            except Exception as e:
                await message.answer(
                    f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет", sizes=(2,))
                await state.clear()


# Хендлер для отлова некорректных вводов для состояния question3
@user_private_router.message(AddRequestCourse.contact_information)
async def add_contact_information_2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст ответа заново!")

#
#
# # Ловим данные для состояние image и потом выходим из состояний
# @admin_router.message(AddProduct.image, or_f(F.photo, F.text == "."))
# async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
#     if message.text and message.text == "." and AddProduct.product_for_change:
#         await state.update_data(image=AddProduct.product_for_change.image)
#
#     elif message.photo:
#         await state.update_data(image=message.photo[-1].file_id)
#     else:
#         await message.answer("Отправьте фото предложения!")
#         return
#     data = await state.get_data()
#     user_id = message.from_user.id
#     try:
#         if AddProduct.product_for_change:
#             await orm_update_product(session, AddProduct.product_for_change.id, data, user_id)
#         else:
#             await orm_add_product(session, data, user_id)
#         await message.answer("Товар добавлен/изменен", reply_markup=get_callback_btns(btns=LEXICON_btn_main_admin_menu, sizes=(2,)))
#         await state.clear()
#
#     except Exception as e:
#         await message.answer(
#             f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет",
#             reply_markup=get_callback_btns(btns=LEXICON_btn_main_admin_menu, sizes=(2,)),
#         )
#         await state.clear()
#
#     AddProduct.product_for_change = None
#
# # Ловим все прочее некорректное поведение для этого состояния
# @admin_router.message(AddProduct.image)
# async def add_image2(message: types.Message, state: FSMContext):
#     await message.answer("Отправьте фото.")
