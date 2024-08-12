
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import User, CourseRequest

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

###############################запрос на курс########################
    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # request_number: Mapped[int] = mapped_column(default=0)
    # question1: Mapped[str] = mapped_column(Text)
    # question2: Mapped[str] = mapped_column(Text)
    # question3: Mapped[str] = mapped_column(Text)
    # contact_information: Mapped[str] = mapped_column(Text)
    # first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    # last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    # username: Mapped[str] = mapped_column(unique=False, nullable=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    #
    # user: Mapped['User'] = relationship(backref='courserequest')





async def orm_add_request_course_information(session: AsyncSession, data: dict, user_id: int,
                                        username: str, last_name: str, first_name: str):
    obj = CourseRequest(
        question1=data['question1'],
        question2=data['question2'],
        question3=data['question3'],
        contact_information=data['contact_information'],
        user_id = user_id,
        username = username,
        last_name = last_name,
        first_name = first_name
    )
    session.add(obj)
    await session.commit()

#
# async def orm_get_notes(session: AsyncSession):
#     query = select(Notes)
#     result = await session.execute(query)
#     return result.scalars().all()
#
#
# async def orm_get_note(session: AsyncSession, note_id: int):
#     query = select(Notes).where(Notes.id == note_id)
#     result = await session.execute(query)
#     return result.scalar()
#
#
#
# async def orm_delete_note(session: AsyncSession, note_id: int):
#     query = delete(Notes).where(Notes.id == note_id)
#     await session.execute(query)
#     await session.commit()
