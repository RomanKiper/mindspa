LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'ГЛАВНОЕ МЕНЮ',
    '/admin': 'АДМИНКА',
    '/help': 'ПОМОЩЬ',
}

LEXICON_HI = {"привет", "здорова", "хай", "приветствую", "добрый день", "здравствуйте", "здрасти", "hi", "hello",
               "good morning", "good day"}

restricted_words = {'дурак', 'осел', 'болван', 'пидор', 'сидор', 'хуй'}


LEXICON_RU: dict[str, str] = {
    '/help': 'Тебе доступны команды:\n'
             '/start - запуск бота.\n'
             '/help - список команд.\n'
             '/description - описание бота.\n'
             '/insta_links - список ссылок на каналы instagram.\n'
             '/tiktok_links - список ссылок на каналы TikTok.\n'
             'Ты можешь воспользваться основным меню!\n'
             '👇👇👇 Меню.'
    ,
    '/admin+panel': '<b>Административная панель.</b>\nТы можешь добавить/изменить/удалить услуги, баннеры, КП, заметки и документы.'
    ,
    '/description_slivki':
        '<b>Сливки бай - это крупнейший маркетплэйс скидок в РБ.</b>\n'
        '✅13 лет на рынке услуг.\n'
        '✅1 000 000+ пользователей на сайте в месяц.\n'
        '✅1 000 000+ установок приложения.\n'
        '✅700 000+ подписчиков в социальных медиа.\n'
        '✅11 000+ партнеров.\n'
        '✅16 Instagram-каналов в РБ.\n'
        '✅30 блогеров в штате.\n'
        '✅40 городов в Беларуси.\n\n'
        '👨‍👨‍👧‍👦Аудитория Сливки Бай - активное население Беларуси со средним доходом и с яркой жизненной позицией.\n'
    ,

    '/office_adress':
        "Адрес:\nг. Минск, Проспект Независимости, 32А, строение 4\n"
        "БЦ 'Проспект' \n"
        "6 этаж\n",

    '/description': '😎Bun_bot - вертуальный специалит по качественному продвижению в компании Сливки бай.\n'
                    '😎Bun_bot даст вам  цены на услуги компании, статистику, покажет примеры,'
                    ' ознакомит вас с основными вариантами размещения на Сливках.\n'
                    '😎Bun_bot является молодым ботом. Он будет развиваться, а объем и качество, предоставляемой им информации, будут расти.'
    ,

    'no_echo': 'Данный тип апдейтов не поддерживается '
               'методом send_copy',

    '/insta_links': '<b>Ссылки на каналы Instagram:</b>\n'
                    '<a href="https://www.instagram.com/slivkiby">www.instagram.com/slivkiby</a>\n'
                    '<a href="https://www.instagram.com/giperspros">www.instagram.com/giperspros</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_beauty/">www.instagram.com/slivkiby_beauty</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_brest">www.instagram.com/slivkiby_brest</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_gomel">www.instagram.com/slivkiby_gomel</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_mogilev">www.instagram.com/slivkiby_mogilev</a>\n'
                    '<a href="https://www.instagram.com/slivki_grodno">www.instagram.com/slivki_grodno</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_vitebsk">www.instagram.com/slivkiby_vitebsk</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_svetlogorsk">www.instagram.com/slivkiby_svetlogorsk</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_pinsk">www.instagram.com/slivkiby_pinsk</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_bobruisk">www.instagram.com/slivkiby_bobruisk</a>\n'
                    '<a href="https://www.instagram.com/slivki_baranovichi">www.instagram.com/slivki_baranovichi</a>\n'
                    '<a href="https://www.instagram.com/slivki_borisov">www.instagram.com/slivki_borisov</a>\n'
                    '<a href="https://www.instagram.com/slivkiby_orsha">www.instagram.com/slivkiby_orsha</a>\n'
                    '<a href="https://www.instagram.com/akcii_skidki_belarus/">www.instagram.com/akcii_skidki_belarus</a>\n'
    ,

    '/telega_links': '<b>Ссылки на каналы Telegram:</b>\n'
                    '<a href="https://t.me/slivki_by">https://t.me/slivki_by</a>\n'
                    '<a href="https://t.me/slivkiby_mogilev">https://t.me/slivkiby_mogilev</a>\n'
                    '<a href="https://t.me/slivkiby_gomel">https://t.me/slivkiby_gomel</a>\n'
                    '<a href="https://t.me/slivkiby_vitebsk">https://t.me/slivkiby_vitebsk</a>\n'
                    '<a href="https://t.me/slivkiby_bobruysk">https://t.me/slivkiby_bobruysk</a>\n'
                    '<a href="https://t.me/slivki_brest">https://t.me/slivki_brest</a>\n'
                    '<a href="https://t.me/slivki_baranovichi">https://t.me/slivki_baranovichi</a>\n'
                    '<a href="https://t.me/slivkiby_grodno">https://t.me/slivkiby_grodno</a>\n'
    ,

    '/agreement_links': '<b>Ссылки на договоры оферты:</b>\n'
                     '<a href="https://www.slivki.by/publichnyj-dogovor-okazaniya-reklamnyh-uslug-i-razmesheniya-akcij">Публичный договор возмездного оказания рекламных услуг</a>\n\n'
                     '<a href="https://www.slivki.by/dogovor-oferta-instagram">Договор оферта инстаграм</a>\n'

    ,

    '/tiktok_links': '<b>Ссылки на каналы TikTok:</b>\n'
                     '<a href="https://www.tiktok.com/@slivkiby">www.tiktok.com/@slivkiby</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_brest">www.tiktok.com/@slivkiby_brest</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_vitebsk">www.tiktok.com/@slivkiby_vitebsk</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_grodno">www.tiktok.com/@slivkiby_grodno</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_gomel">www.tiktok.com/@slivkiby_gomel</a>\n'
                     '<a href="https://www.tiktok.com/@slivkimogilev">www.tiktok.com/@slivkimogilev</a>\n'
                     '<a href="https://www.tiktok.om/@slivkiby_bobruysk">www.tiktok.om/@slivkiby_bobruysk</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_borisov">www.tiktok.com/@slivkiby_borisov</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_baranovichi">www.tiktok.com/@slivkiby_baranovichi</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_pinsk">www.tiktok.com/@slivkiby_pinsk</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_svetlogorsk">www.tiktok.com/@slivkiby_svetlogorsk</a>\n'
                     '<a href="https://www.tiktok.com/@slivkiby_orsha">www.tiktok.com/@slivkiby_orsha</a>\n'
    ,
    '/list_links_work_tables': '<b>Рабочие таблицы/регламенты(только для работкников  Slivkiby):</b>\n\n'
                               '<a href="https://docs.google.com/spreadsheets/d/13lJebGgLptSelDHMcb_-QWP3SfQQ2TNry1td0qFTPBk/edit#gid=654343601">Таблица инстаграм.</a>\n\n'
                               '<a href="https://docs.google.com/spreadsheets/d/1BWHJ3xwKwhtMKApPSwXHpF2s2wifQ1Xregtj7zfaJ1A/edit#gid=1293730834">Дневные отчеты/посещаемость.</a>\n\n'
                               '<a href="https://docs.google.com/spreadsheets/d/1hHsBoWh8uM9ENREd2ARvIxlH0AwcYuH6PcxrCDDbiXw/edit?userstoinvite=roman@slivki.by&sharingaction=manageaccess&role=writer#gid=443600561">Большая таблица.</a>\n\n'
                               '<a href="https://docs.google.com/document/d/12wgVsiGgn-3IuwG3n2p7RpEgN69u_-7d9w60vk3KubQ/edit?pli=1#heading=h.6vbdo72hsqbe">Условия работы/регламенты.</a>\n\n'

}

LEXICON_btn_main_menu: dict[str, str] = {
        "ЦЕНЫ/СТАТИСТИКА🤑💵": "price_statistic",
        "О НАС": "about",
        "FAQ🤯": "faq_main",
        "БЛОГЕРЫ👩‍🎤": "blogers-main",
        "ССЫЛКИ🔗": "links_main",
        "КОНТАКТЫ": "contacts_main",
        "ПРЕЗЕНТАЦИЯ🎁": "presentation_main",
    }

LEXICON_btn_help: dict[str, str] = {
        "Инструкция для админки📄": "adm_panel_instruction",
        "Связь с администратором📞": "adm_connect",
        "Общая информация🪬": "main_information",
    }

