from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import (User, CourseRequest, CodeMissin, CanNotEnterAccaunt, BadCode,
                             WhereEnterCode, NoQuestion)


##################### Добавляем юзера в БД #####################################

async def orm_add_user(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        phone: str | None = None,
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, first_name=first_name, last_name=last_name, phone=phone, username=username)
        )
        await session.commit()


async def orm_get_users(session: AsyncSession, user_id: int):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_add_request_course_information(session: AsyncSession, data: dict, user_id: int,
                                             username: str, last_name: str, first_name: str):
    query = delete(CourseRequest).where(CourseRequest.user_id == user_id)
    await session.execute(query)
    await session.commit()
    obj = CourseRequest(
        question1=data['question1'],
        question2=data['question2'],
        question3=data['question3'],
        user_id=user_id,
        username=username,
        last_name=last_name,
        first_name=first_name
    )
    session.add(obj)
    await session.commit()


async def orm_add_code_missing_information(session: AsyncSession, data: dict, user_id: int,
                                           username: str, last_name: str, first_name: str):
    query = delete(CodeMissin).where(CodeMissin.user_id == user_id)
    await session.execute(query)
    await session.commit()
    obj = CodeMissin(
        mail_user=data['sending_mail'],
        user_id=user_id,
        username=username,
        last_name=last_name,
        first_name=first_name
    )
    session.add(obj)
    await session.commit()


async def orm_add_information_whereentercode(session: AsyncSession, user_id: int,
                                           username: str, last_name: str, first_name: str):
    query = delete(WhereEnterCode).where(WhereEnterCode.user_id == user_id)
    await session.execute(query)
    await session.commit()
    obj = WhereEnterCode(
        user_id=user_id,
        username=username,
        last_name=last_name,
        first_name=first_name
    )
    session.add(obj)
    await session.commit()


async def orm_add_info_badcode(session: AsyncSession, user_id: int,
                               username: str, last_name: str, first_name: str):
    query = delete(BadCode).where(BadCode.user_id == user_id)
    await session.execute(query)
    await session.commit()
    obj = BadCode(
        user_id=user_id,
        username=username,
        last_name=last_name,
        first_name=first_name
    )
    session.add(obj)
    await session.commit()


async def orm_add_info_noquestion(session: AsyncSession, data: dict, user_id: int,
                                           username: str, last_name: str, first_name: str):
    query = delete(NoQuestion).where(NoQuestion.user_id == user_id)
    await session.execute(query)
    await session.commit()
    obj = NoQuestion(
        question_user=data['new_question'],
        user_id=user_id,
        username=username,
        last_name=last_name,
        first_name=first_name
    )
    session.add(obj)
    await session.commit()


async def orm_add_information_cannotlogin(session: AsyncSession, data: dict, user_id: int,
                                          username: str, last_name: str, first_name: str):
    query = delete(CanNotEnterAccaunt).where(CanNotEnterAccaunt.user_id == user_id)
    await session.execute(query)
    await session.commit()
    obj = CanNotEnterAccaunt(
        mail_user=data['log_sending_mail'],
        user_id=user_id,
        username=username,
        last_name=last_name,
        first_name=first_name
    )
    session.add(obj)
    await session.commit()
