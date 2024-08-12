from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    id_admins_mindspa: list[int]  # Список id администраторов бота
    id_chat_admin: int
    id_admin_developer: int


@dataclass
class Config:
    tg_bot: TgBot


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            id_admins_mindspa=list(map(int, env.list('ID_ADMINS_MINDSPA'))),
            id_chat_admin=env('ID_CHAT_ADMIN'),
            id_admin_developer=env('ID_ADMIN_DEVELOPER'),
        )
    )