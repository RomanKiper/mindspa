import json

from sqlalchemy import String, Float, Text, DateTime, func, ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "user"

    # Телеграм user_id
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)


class CourseRequest(Base):
    __tablename__ = 'courserequest'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_number: Mapped[int] = mapped_column(default=0)
    question1: Mapped[str] = mapped_column(Text)
    question2: Mapped[str] = mapped_column(Text)
    question3: Mapped[str] = mapped_column(Text)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

    user: Mapped['User'] = relationship(backref='courserequest')


class CodeMissin(Base):
    __tablename__ = 'codemissing'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_number: Mapped[int] = mapped_column(default=0)
    mail_user: Mapped[str] = mapped_column(String(150))
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

    user: Mapped['User'] = relationship(backref='codemissing')


class WhereEnterCode(Base):
    __tablename__ = 'whereentercode'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_number: Mapped[int] = mapped_column(default=0)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

    user: Mapped['User'] = relationship(backref='whereentercode')


class BadCode(Base):
    __tablename__ = 'badcode'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_number: Mapped[int] = mapped_column(default=0)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

    user: Mapped['User'] = relationship(backref='badcode')


class CanNotEnterAccaunt(Base):
    __tablename__ = 'cannotenteraccaunt'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_number: Mapped[int] = mapped_column(default=0)
    mail_user: Mapped[str] = mapped_column(String(150))
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

    user: Mapped['User'] = relationship(backref='cannotenteraccaunt')


class NoQuestion(Base):
    __tablename__ = 'noquestion'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_number: Mapped[int] = mapped_column(default=0)
    question_user: Mapped[str] = mapped_column(Text)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

    user: Mapped['User'] = relationship(backref='noquestion')


class HandlerCounter(Base):
    __tablename__ = 'handler_counter'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    handler_name: Mapped[str] = mapped_column(String(150), nullable=False)
    count: Mapped[int] = mapped_column(default=0)

    user: Mapped['User'] = relationship(backref='handler_counter')
