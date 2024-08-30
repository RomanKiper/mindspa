LEXICON_COMMANDS: dict[str, str] = {
    '/questions': '🚀 СТАРТ',
}

PDF_FILE_ANDR_INTR = 'BQACAgIAAxkBAAIIMmbFDUPRAz8CGrUZje1TWoEUS9hbAAKEYAACDaIoSqqho5ArFvLJNQQ'
PDF_FILE_IPHONE_INTR = 'BQACAgIAAxkBAAIIWWbFFGUlrWdgjkNQQ0WMRj4d7clyAALVTgACDaIwSkWx8ODiA0YpNQQ'
VIDEO_FILE_ANDR_INTR = 'BAACAgIAAxkBAAIJ1WbIKjyq61_V0SZlvXE6pw8JLvP_AALBVwACEOFAShvt1mgxAljINQQ'
VIDEO_FILE_IPHONE_INTR = 'BAACAgIAAxkBAAIJ2GbIKksAAZ_iMsFPHbtFFKx0j2htVwACwlcAAhDhQEqlZJ4IE9903TUE'

LEXICON_btn_questions: dict[str, str] = {
    "Мне нужна помощь с подбором курса": "help_with_course",
    "Не пришел код": "do_not_have_code",
    "Не понимаю, куда вводить код": "do_not_now_how_to_enter_code",
    "Мне пришел код, но он не работает": "bad_code",
    "Не могу войти в аккаунт": "can_not_enter_account",
    "Моего вопроса нет в списке": "no_my_question",
}

LEXICON_btn_answer_questions: dict[str, str] = {
    "Ответить на вопросы": "first_question_form",
    "Назад ко всем вопросам": "main_list_questions",
}

LEXICON_btn_helh_with_code: dict[str, str] = {
    "Отправить адрес эл.почты": "send_mail_adress",
    "Спасибо мой вопрос решен": "question_is_solved",
    "Назад ко всем вопросам": "main_list_questions",
}

LEXICON_btn_code_do_not_work: dict[str, str] = {
    "Моя проблема решена": "problem_is_solved",
    "Моя проблема НЕ решена": "problem_is_not_solved",
    "Назад ко всем вопросам": "main_list_questions",
}

LEXICON_btn_model_phone: dict[str, str] = {
    "Android": "android_phone",
    "Iphone": "iphone_phone",
}

LEXICON_btn_back_to_questions: dict[str, str] = {
    "Вернуться ко всем вопросам": "main_list_questions"
}

LEXICON_btn_back_and_video_android: dict[str, str] = {
    "Видеоинструкция": "video_android",
    "Вернуться ко всем вопросам": "main_list_questions",
}

LEXICON_btn_back_and_video_iphone: dict[str, str] = {
    "Видеоинструкция": "video_iphone",
    "Вернуться ко всем вопросам": "main_list_questions",
}

LEXICON_btn_logging_instruction: dict[str, str] = {
    "Моя проблема решена": "log_problem_is_solved",
    "Моя проблема НЕ решена": "log_send_mail_to_admin",
    "Назад ко всем вопросам": "main_list_questions",
}

LEXICON_btn_no_my_question: dict[str, str] = {
    "Написать администратору": "write_new_question",
    "Назад ко всем вопросам": "main_list_questions",
}

LEXICON_btn_main_admin_menu: dict[str, str] = {
    "Отчет": "report_admin",
    "Инструкция": "instruction_admin",
}

LEXICON_btn_BACK_main_admin_menu: dict[str, str] = {
    "НАЗАД В АДМИНКУ": "admin_menu",
}

LEXICON_RU: dict[str, str] = {
    '/question_list': '<b>Спасибо за интерес к курсам Mindspa!</b>\n'
                      '<b>Пожалуйста, выбери свой вопрос в списке ниже.</b>\n\n'
                      '<i>Продолжая использование бота, ты соглашаешься на обработку своих персональных данных в соответствии'
                      "<a href='https://mindspa.me/politika-konfidencialnosti/'> с политикой конфиденциальности</a>.</i>\n"

    ,
    '/help_with_course': '<b>Мне нужна помощь с подбором курса.</b> \n\n'
                         'Ответь на несколько вопросов. Это поможет нам подобрать курс, который сможет решить твой запрос.\n\n'
                         # '✅1.Проблема, которую я хочу решить — ...\n'
                         # '✅2.Как проявляется твоя проблема в мыслях, чувствах, ощущениях, поведении?\n'
                         # '✅3.Результат, которого я хочу достичь — ...\n\n'
                         'Постарайся ответить на каждый вопрос развернуто — 2-3 предложениями. '
                         'Так мы сможем лучше понять, что тебя беспокоит.'
                         # 'Наш психолог даст тебе обратную связь в течение несколько часов, в редких случаях в срок до 24 часов.\n\n'
    ,
    '/help_with_code': '<b>Не пришел код.</b>\n\n'
                       'Проверь папку <b>«Спам»</b>. Иногда письма с кодом и инструкцией по активации попадают туда.\n\n'
                       'Если письма там нет или в таблице отсутствует код, пожалуйста, пришли электронный адрес, который был указан при покупке.\n'
    ,
    '/answer_about_code': '<b>Спасибо!</b>\n'
                          'Твой запрос и адрес электронной почты переданы в службу технической поддержки.\n\n'
                          'Доступ поступит на указанную тобой электронную почту. '
                          'Обычно это занимает несколько часов, в редких случаях — до 24 часов.\n'

    ,
    '/bad_code': '<b>Мне пришел код, но он не работает.</b>\n\n'
                 'Если в коде есть цифра <b>0</b>, убедись, что вводишь именно ее, а не букву <b>О</b>.\n\n'
                 'После активации, даже если у тебя появилась надпись  <b>«неверный код»</b>, обязательно закрой приложение'
                 ' и снова открой.\n\nПосле этого проверь раздел <b>«Активированы»</b>.\n'
    ,
    '/bad_code_problem_solved': 'Спасибо, что выбираешь нас!\n'
                                'Желаем тебе успеха в прохождении курса.\n'
    ,
    '/bad_code_problem_not_solved': '<b>Спасибо!</b>\n'
                                    'Твой запрос и ссылка на твой телеграм переданы  в службу технической поддержки.\n\n'
                                    'Наш консультант скоро свяжется с тобой. Обычно это занимает несколько часов, в редких случаях — до 24 часов.\n'
    ,
    '/instruction_entering_code': '<b>Не понимаю, куда вводить код.</b>\n\n'
                                  'Если у тебя еще нет приложения Mindspa — <a href="http://onelink.to/mindspa"><i>скачай</i></a> его и самостоятельно зарегистрируйся.\n\n'
                                  'Выбери модель своего телефона.\n'
    ,
    '/log_code_answer': '<b>Спасибо!</b>\n'
                        'Твой запрос и адрес переданы в службу технической поддержки.\n\n'
                        "Временный пароль поступит на указанную тобой электронную почту.\n"
                        "После его можно будет изменить в настройках.\n\n"
                        "Обычно срок получения ответа занимает несколько часов, в редких случаях — до 24 часов."
    ,

    '/instruction_entering_accaunt': '<b>Не могу войти в аккаунт.</b>\n\n'
                                     'Попробуй восстановить доступ через кнопку <b>«Забыли пароль»</b>.\n\n'
                                     'Если возникают сложности или письмо с временным паролем не приходит,'
                                     ' пожалуйста, пришли электронный адрес, который был указан при регистрации.\n'
    ,
    '/no_my_question': '<b>Моего вопроса нет в списке.</b>\n\n'
                       'Если тебе не удалось найти ответ на свой вопрос, напиши нам об этом.\n\n'
                       'Наш консультант поможет во всем разобраться.\n\n'
                       'Обычно мы отвечаем в течение часа, в редких случаях — в течение 4-х часов.\n'
    ,
    '/finish_answer': '<b>Спасибо!</b>\n'
                      'Твой запрос передан в службу поддержки.\n\n'
                      "Наш консультант поможет во всем разобраться.\n"
                      "Обычно мы отвечаем в течение часа, в редких случаях — в течение 4-х часов.\n"
    ,
    '/instruction_android': '<b>Android</b>\n'
                            '✅В главном меню (внизу) нажми на «Профиль».\n'
                            '✅Теперь вверху нажми на Колесико.\n'
                            '✅Нажми на Промо-код.\n'
                            '✅Введи код (он указан в письме, которое пришло на почту после оплаты).\n'
                            '✅Перейди в раздел Курсы, вкладка «Активированы».\n'
    ,
    '/instruction_iphone': '<b>Iphone</b>\n'
                           "<a href='https://coupon.mindspa.me/ru'>✅<i>Перейди на сайт</i></a>.\n"
                           '✅Введи свой логин и пароль от приложения Mindspa (строго те, что были использованы при регистрации).\n'
                           '✅Введи код (он указан в письме, которое пришло на почту после оплаты).\n'
                           '✅Открой приложение Mindspa.\n'
                           '✅Перейди в раздел Курсы, вкладка «Активированы».\n'
}

LEXICON_ADMIN: dict[str, str] = {
    '/admin+panel': '<b>Административная панель❗</b>\n'
                    'Доступ в данную панель есть только у пользователей с правами админа.\n'
                    'Если ты узнаешь, что кто-то зашел в администативную панель без прав админа, сообщи об этом разработчику❗\n'
    ,
    '/instruction_description': '<b>Инструкция для админа.</b>\n'
                                'Доступ в данную панель есть только у пользователей с правами админа.\n\n'
                                'Полезные команды, которые можно вводить в строку ввода:\n'
                                '✅<b>Отмена</b> - команда, которая выводит бота из "машины состояния". '
                                'Это стостяние когда пользователь заполняет форму для отправки админу.\n'
                                '✅<b>Назад</b> - команда, позволяющая возьзователю вернуться назад на один шаг,'
                                ' кога он заполняет форму для отправки админу.\n'
                                '✅<b>admin, administrator, админ, администратор</b> - команды вызова административвной панели.\n'
                                '✅<b>вопросы, вопрос, questions, старт, start, начать</b> - команды вызова основного списка вопросов.'
}
