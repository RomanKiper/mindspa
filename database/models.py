import json

from sqlalchemy import String, Float, Text, DateTime, func, ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

#
# class Banner(Base):
#     __tablename__ = 'banner'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(64), unique=True)
#     description: Mapped[str] = mapped_column(Text, nullable=True)
#     image: Mapped[str] = mapped_column(String(150), nullable=True)
#
#
# class Category(Base):
#     __tablename__ = 'category'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)


#
# class Product(Base):
#     __tablename__ = 'product'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     description: Mapped[str] = mapped_column(Text)
#     price: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
#     image: Mapped[str] = mapped_column(String(150))
#     category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
#
#     category: Mapped['Category'] = relationship(backref='product')
#     user: Mapped['User'] = relationship(backref='product')
#
#
#
# class Faq(Base):
#     __tablename__ = 'faq'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     description: Mapped[str] = mapped_column(Text)
#
#
# class Notes(Base):
#     __tablename__ = 'notes'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     description: Mapped[str] = mapped_column(Text)
#
#
# class Bloger(Base):
#     __tablename__ = 'bloger'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     description: Mapped[str] = mapped_column(Text)
#     image: Mapped[str] = mapped_column(String(150))
#
#
# class Video_review(Base):
#     __tablename__ = 'video_review'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(Text)
#     video: Mapped[str] = mapped_column(String(150))
#
#
# class Document(Base):
#     __tablename__ = 'documents'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     document: Mapped[str] = mapped_column(String(150))
#
#
# class Price(Base):
#     __tablename__ = 'prices'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     price: Mapped[str] = mapped_column(String(150))
#
#
# class HandlerCounter(Base):
#     __tablename__ = 'handler_counter'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
#     first_name: Mapped[str] = mapped_column(String(150), nullable=True)
#     last_name: Mapped[str] = mapped_column(String(150), nullable=True)
#     username: Mapped[str] = mapped_column(unique=False, nullable=True)
#     handler_name: Mapped[str] = mapped_column(String(150), nullable=False)
#     count: Mapped[int] = mapped_column(default=0)
#
#     user: Mapped['User'] = relationship(backref='handler_counter')



class User(Base):
    __tablename__ = "user"

    # Телеграм user_id
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(unique=False, nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)


# # Корзина, т.е сущность объединяющая предложения, товары.
# class Cart(Base):
#     __tablename__ = 'cart'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
#     product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
#     quantity: Mapped[int]
#
#     user: Mapped['User'] = relationship(backref='cart')
#     product: Mapped['Product'] = relationship(backref='cart')
#
#
# class Offer(Base):
#     __tablename__ = 'offer'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     description: Mapped[str] = mapped_column(Text)
#     description2: Mapped[str] = mapped_column(Text)
#     price: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
#     price_with_discont: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
#     discont: Mapped[int]
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
#
#     cart_product_list_ids: Mapped[str] = mapped_column(Text)   # список id и колич-ва каждого товара. Список словарей.
#
#     user: Mapped['User'] = relationship(backref='offer')
#
#     def serialize_cart_product_list_ids(self, cart_product_list_ids):
#         return json.dumps(cart_product_list_ids)
#
#     def deserialize_cart_product_list_ids(self, serialized_cart_product_list_ids):
#         return json.dumps(serialized_cart_product_list_ids)
#
#     def save_cart_product_list_ids(self, cart_product_list_ids):
#         self.cart_product_list_ids = self.serialize_cart_product_list_ids(cart_product_list_ids)
#
#
#     def load_cart_product_list_ids(self):
#         return self.deserialize_cart_product_list_ids(self.cart_product_list_ids)