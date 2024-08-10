from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from keyboards.inline.inline import get_callback_btns
from lexicon.lexicon import LEXICON_btn_questions, LEXICON_RU, LEXICON_btn_answer_questions

from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


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

# async def start_cmd(message: types.Message):
#     await message.answer(text=LEXICON_RU["/question_list"],
#                                   reply_markup=get_callback_btns(btns=LEXICON_btn_questions, sizes=(1,)))
#     await message.delete()


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

    product_for_change = None



    texts = {
        'AddRequestCourse:question1': 'Ответьте на вопрос №1 - "Проблема, которую я хочу решить - ...", заново.',
        'AddRequestCourse:question2': 'Ответьте на вопрос №2 - "Моя проблема выражается в....", заново.',
        'AddRequestCourse:question3': 'Ответьте на вопрос №3 - "ПРезультат, которого я хочу достичь — ...", заново.',

        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }

    # Вернутся на шаг назад (на прошлое состояние)
    # Прописано для двух машин состояний: из make_offer и add_product
    @user_private_router.message(StateFilter("*"), Command("назад"))
    @user_private_router.message(StateFilter("*"), F.text.casefold() == "назад")
    async def back_step_handler(message: types.Message, state: FSMContext) -> None:
        current_state = await state.get_state()

        if current_state in (
        AddRequestCourse.question1):
            await message.answer(
                'Предидущего шага нет, или введите название или напишите "отмена"'
            )
            return

        elif current_state == AddNote.description:
            await state.set_state(AddNote.name)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddNote.texts[AddNote.name]}"
            )
            return

        elif current_state == Add_price.price:
            await state.set_state(Add_price.name)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {Add_price.texts[Add_price.name]}"
            )
            return

        elif current_state == Add_document.document:
            await state.set_state(Add_document.name)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {Add_document.texts[Add_document.name]}"
            )
            return

        elif current_state == AddOffer.description:
            await state.set_state(AddOffer.name)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddOffer.texts[AddOffer.name]}"
            )
            return

        elif current_state == AddOffer.making_offer or current_state == AddOffer.discount:
            await state.set_state(AddOffer.description)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddOffer.texts[AddOffer.description]}"
            )
            return


        elif current_state == AddProduct.price:
            await state.set_state(AddProduct.description)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[AddProduct.description]}"
            )
            return


        elif current_state == Add_FAQ.description:
            await state.set_state(Add_FAQ.name)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {Add_FAQ.texts[Add_FAQ.name]}"
            )
            return

        previous = None
        for step in AddProduct.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await message.answer(
                    f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}"
                )
                return
            previous = step
























#
#
# @user_private_router.message(F.text.lower().in_({'старт', 'начать', "start"}))
# @user_private_router.message(CommandStart())
# @user_private_router.callback_query(lambda c: c.data.startswith("main_menu"))
#
# async def start_cmd(message_or_callback: types.Union[types.Message, CallbackQuery], session: AsyncSession):
#     if isinstance(message_or_callback, types.Message):
#         message = message_or_callback
#         await orm_add_user(session,
#                            user_id=message.from_user.id,
#                            username=message.from_user.username,
#                            first_name=message.from_user.first_name,
#                            last_name=message.from_user.last_name,
#                            )
#         await orm_increment_handler_counter(session,
#                                             user_id=message.from_user.id,
#                                             handler_name='start',
#                                             username=message.from_user.username,
#                                             first_name=message.from_user.first_name,
#                                             last_name=message.from_user.last_name,
#                                             )
#         query = select(Banner).where(Banner.name == 'main')
#         result = await session.execute(query)
#         banner = result.scalar()
#         await message.answer_photo(photo=banner.image,
#                                    caption=banner.description,
#                                    reply_markup=get_callback_btns(btns=LEXICON_btn_main_menu, sizes=(1,2,)))
#         await message.delete()
#     elif isinstance(message_or_callback, CallbackQuery):
#         # Если это колбэк-запрос
#         callback = message_or_callback
#         await orm_add_user(session,
#                            user_id=callback.message.from_user.id,
#                            username=callback.message.from_user.username,
#                            first_name=callback.message.from_user.first_name,
#                            last_name=callback.message.from_user.last_name,
#                            )
#         query = select(Banner).where(Banner.name == 'main')
#         result = await session.execute(query)
#         banner = result.scalar()
#         await callback.message.answer_photo(photo=banner.image,
#                                    caption=banner.description,
#                                    reply_markup=get_callback_btns(btns=LEXICON_btn_main_menu, sizes=(1,2,)))
#         await callback.message.delete()
#
# #
# # @user_private_router.callback_query(F.data == 'price_statistic')
# # async def get_list_advertising_menu(callback: types.CallbackQuery):
# #
# #     await callback.message.answer(text="В данном блоке ты получшиь цены, статистику и примеры размещения рекламы.",
# #                                   reply_markup=get_callback_btns(btns=LEXICON_btn_price_statistic, sizes=(2,)))
# #     await callback.message.delete()
# #
# #
# # @user_private_router.callback_query(F.data == 'about')
# # async def get_info_about(callback: types.CallbackQuery):
# #     await callback.message.answer(text=LEXICON_RU['/description_slivki'], reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_main_menu, sizes=(2,)))
# #     await callback.message.delete()
# #
# #
# # @user_private_router.message(F.text.lower().in_({'помощь', "help"}))
# # @user_private_router.message(Command('help'))
# # async def help_cmd(message: types.Message):
# #     await message.answer(text="Сделайте выбор:", reply_markup=get_callback_btns(btns=LEXICON_btn_help, sizes=(1,)))
# #
# #
# # @user_private_router.message(F.text.lower().in_(LEXICON_HI))
# # async def hi_cmd(message: types.Message):
# #     await message.answer("И тебя приветствую!")
# #
# #
# # ############################################## часто задаваемые вопросы в общем доступе ###################
# # @user_private_router.callback_query(F.data == 'faq_main')
# # async def admin_features(callback: types.CallbackQuery, session: AsyncSession):
# #     faqs = await orm_get_faqs(session)
# #     if len(faqs) > 0:
# #         btns = {faq.name: f'faq2_{faq.id}' for faq in faqs}
# #         back_to_main_menu = InlineKeyboardButton(text="НАЗАД", callback_data="main_menu")
# #         markup = get_callback_btns_extra_btn(btns=btns, extra_buttons=[back_to_main_menu])
# #         await callback.message.answer("Часто задаваемые вопросы:", reply_markup=markup)
# #     else:
# #         await callback.message.answer("Список часто задаваемых вопросв пуст🤔.\nДобавьте вопросы через администартивную панель.📝")
# #
# #
# #
# # @user_private_router.callback_query(F.data.startswith('faq2_'))
# # async def starring_at_product(callback: types.CallbackQuery, session: AsyncSession):
# #     faq_id = callback.data.split('_')[-1]
# #     faq_item = await orm_get_faq(session, int(faq_id))
# #     await callback.message.answer(
# #         f"<strong>{faq_item.name}</strong>\n\n"
# #         f"{faq_item.description}\n\n",
# #         reply_markup=get_callback_btns(
# #             btns={
# #                 "Назад": f"faq_main",
# #             },
# #             sizes=(2,)
# #         ),
# #     )
# #     await callback.answer()
# #
# # ######################################ссылки ######################################
# #
# # @user_private_router.callback_query(F.data == 'links_main')
# # async def get_main_menu_links(callback: types.CallbackQuery):
# #     await callback.message.answer(text="Рабочие ссылки компании.", reply_markup=get_callback_btns(btns=LEXICON_btn_main_links, sizes=(1,2,2,2,2,1)))
# #     await callback.message.delete()
# #
# #
# # @user_private_router.callback_query(F.data == 'site_slivki_link')
# # async def get_site_slivki_link(callback: types.CallbackQuery):
# #     await callback.message.answer(text="Ссылка на сайт Сливки Бай", reply_markup=get_inlineMix_btns(btns=LEXICON_btn_slivki_site_link, sizes=(1,)) )
# #     disable_web_page_preview = True
# #     await callback.message.delete()
# #
# #
# # @user_private_router.callback_query(F.data == 'app-link')
# # async def get_app_link(callback: types.CallbackQuery):
# #     await callback.message.answer(text="Ссылка на скачивание мобильного приложения slivkiby", reply_markup=get_inlineMix_btns(btns=LEXICON_btn_app_link, sizes=(1,)) )
# #     disable_web_page_preview = True
# #     await callback.message.delete()
# #
# #
# # @user_private_router.callback_query(F.data == 'insta_all_links')
# # async def get_all_insta_links(callback: types.CallbackQuery):
# #     await callback.message.answer(text=LEXICON_RU['/insta_links'], disable_web_page_preview=True,
# #                                   reply_markup=get_inlineMix_btns(btns=LEXICON_btn_back_menu_links, sizes=(1,)) )
# #     await callback.message.delete()
# #
# #
# # @user_private_router.message(Command('insta_links'))
# # async def get_all_insta_links(message: types.Message):
# #     await message.answer(text=LEXICON_RU['/insta_links'], disable_web_page_preview=True,
# #                                   reply_markup=get_inlineMix_btns(btns=LEXICON_btn_back_to_advertising_menu, sizes=(1,)) )
# #     await message.delete()
# #
# #
# # @user_private_router.callback_query(F.data == 'tiktok_all_links')
# # async def get_all_tiktok_links(callback: types.CallbackQuery):
# #     await callback.message.answer(text=LEXICON_RU['/tiktok_links'], disable_web_page_preview=True,
# #                                   reply_markup=get_inlineMix_btns(btns=LEXICON_btn_back_menu_links, sizes=(1,)) )
# #     await callback.message.delete()
# #
# #
# # @user_private_router.message(Command('tiktok_links'))
# # async def get_all_tiktok_links(message: types.Message):
# #     await message.answer(text=LEXICON_RU['/tiktok_links'], disable_web_page_preview=True,
# #                                   reply_markup=get_inlineMix_btns(btns=LEXICON_btn_back_to_advertising_menu, sizes=(1,)) )
# #     await message.delete()
# #
# #
# # @user_private_router.callback_query(F.data == 'telegram_all_links')
# # async def get_all_telegram_links(callback: types.CallbackQuery):
# #     await callback.message.answer(text=LEXICON_RU['/telega_links'], disable_web_page_preview=True,
# #                                   reply_markup=get_inlineMix_btns(btns=LEXICON_btn_back_menu_links, sizes=(1,)) )
# #     await callback.message.delete()
# #
# #
# # @user_private_router.callback_query(F.data == 'agreement_links')
# # async def get_agreement_links(callback: types.CallbackQuery):
# #     await callback.message.answer(text=LEXICON_RU['/agreement_links'], disable_web_page_preview=True,
# #                                   reply_markup=get_inlineMix_btns(btns=LEXICON_btn_back_menu_links, sizes=(1,)) )
# #     await callback.message.delete()
# #
# #
# # # перенес в admin_add_product  для того чтобы досту был только у админов
# # # @user_private_router.callback_query(F.data == 'tables_links')
# # # async def get_tables_links(callback: types.CallbackQuery):
# # #     await callback.message.answer(text=LEXICON_RU['/list_links_work_tables'], disable_web_page_preview=True,
# # #                                   reply_markup=get_inlineMix_btns(btns=LEXICON_btn_back_menu_links, sizes=(1,)) )
# # #     await callback.message.delete()
# #
# #
# # ###################################################################
# #
# # @user_private_router.callback_query(F.data == 'contacts_main')
# # async def inline_get_office_information(callback: types.CallbackQuery, bot: Bot):
# #     await bot.send_location(chat_id=callback.from_user.id,
# #                             latitude=53.904278,
# #                             longitude=27.569655)
# #     await callback.message.answer(text=LEXICON_RU['/office_adress'],
# #                                   reply_markup=get_callback_btns(btns=LEXICON_btn_back_to_main_menu, sizes=(2,)))
# #     await callback.message.delete()
# #
# # #################################################################
# #
# # @user_private_router.callback_query(F.data == 'presentation_main')
# # async def get_presentation_page1(callback: types.CallbackQuery):
# #     await callback.message.answer(text=LEXICON_PRESENTATION['/present1'],
# #                                   reply_markup=get_inlineMix_btns(btns=LEXICON_btn_presentation1, sizes=(1,)) )
# #     await callback.message.delete()
# #
# #
# # # @user_private_router.message()
# # # async def send_echo(message: Message):
# # #     try:
# # #         if message.photo:
# # #             await message.send_copy(chat_id=message.chat.id)
# # #             photo_id = message.photo[0].file_id
# # #             await message.answer(f"ID фотографии: {photo_id}")
# # #         elif message.video:
# # #             await message.send_copy(chat_id=message.chat.id)
# # #             video_id = message.video.file_id
# # #             await message.answer(f"ID видео: {video_id}")
# # #     except TypeError:
# #         await message.reply(text=LEXICON_RU['no_echo'])