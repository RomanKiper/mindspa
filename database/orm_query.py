
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Product, Category, Banner, Cart, User, Offer, Faq, Price, Document, Notes, HandlerCounter


########################### счетчик  #########################

async def orm_increment_handler_counter(session: AsyncSession, user_id: int, handler_name: str,
                                        username: str, last_name: str, first_name: str):
    usage = await session.execute(
        select(HandlerCounter).filter_by(user_id=user_id, handler_name=handler_name)
    )
    usage = usage.scalars().first()

    if usage:
        usage.count += 1
    else:
        usage = HandlerCounter(user_id=user_id, handler_name=handler_name, count=1, username=username,
                               last_name=last_name, first_name=first_name)
        session.add(usage)

    await session.commit()


########################### работа с продуктом #########################

async def orm_add_product(session: AsyncSession(), data: dict, user_id: int):
    obj = Product(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image'],
        category_id=int(data["category"]),
        user_id=user_id,
    )
    session.add(obj)
    await session.commit()


async def orm_get_products(session: AsyncSession, category_id, user_id):
    query = select(Product).where(Product.category_id == int(category_id)).where(Product.user_id == int(user_id))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_products_in_offer(session: AsyncSession, pr_id):
    query = select(Product).where(Product.id == int(pr_id))
    result = await session.execute(query)
    return result.scalar()


async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_product(session: AsyncSession, product_id: int, data, user_id: int):
    query = update(Product).where(Product.id == product_id).values(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image'],
        category_id=int(data["category"]),
        user_id=user_id,
    )

    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()


############### Работа с баннерами (информационными страницами) ###############

async def orm_add_banner_description(session: AsyncSession, data: dict):
    #Добавляем новый или изменяем существующий по именам
    #пунктов меню: main, about, cart, shipping, payment, catalog
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description=description) for name, description in data.items()])
    await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()


############################ Категории ######################################

async def orm_get_categories(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories])
    await session.commit()


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

######################## Работа с корзинами #######################################

async def orm_add_to_cart(session: AsyncSession, user_id: int, product_id: int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).options(joinedload(Cart.product))
    cart = await session.execute(query)
    cart = cart.scalar()
    if cart:
        cart.quantity += 1
        await session.commit()
        return cart
    else:
        session.add(Cart(user_id=user_id, product_id=product_id, quantity=1))
        await session.commit()



async def orm_get_user_carts(session: AsyncSession, user_id):
    query = select(Cart).filter(Cart.user_id == user_id).options(joinedload(Cart.product))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_from_cart(session: AsyncSession, user_id: int, product_id: int):
    query = delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    await session.execute(query)
    await session.commit()

async def orm_delete_all_carts(session: AsyncSession, user_id: int):
    query = delete(Cart).filter(Cart.user_id == user_id).options(joinedload(Cart.product))
    await session.execute(query)
    await session.commit()


async def orm_reduce_product_in_cart(session: AsyncSession, user_id: int, product_id: int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).options(joinedload(Cart.product))
    cart = await session.execute(query)
    cart = cart.scalar()

    if not cart:
        return
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await orm_delete_from_cart(session, user_id, product_id)
        await session.commit()
        return False

######################## Работа с  кп #######################################



async def orm_add_offer(session: AsyncSession(), data: dict):
    obj = Offer(
        name=data['name'],
        description=data['description'],
        description2=data['making_offer'],
        discont=data['discount'],
    )
    session.add(obj)
    await session.commit()


async def orm_get_offers(session: AsyncSession, user_id: int):
    query = select(Offer).where(Offer.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_offers_id(session: AsyncSession, offer_id: int):
    query = select(Offer).where(Offer.id == int(offer_id))
    result = await session.execute(query)
    return result.scalar()


async def orm_delete_offer(session: AsyncSession, offer_id: int, user_id: int):
    query = delete(Offer).where(Offer.user_id == user_id, Offer.id == int(offer_id))
    await session.execute(query)
    await session.commit()


######################## Работа с  FAQ #######################################



async def orm_add_faq(session: AsyncSession(), data: dict):
    obj = Faq(
        name=data['name'],
        description=data['description'],
    )
    session.add(obj)
    await session.commit()


async def orm_get_faqs(session: AsyncSession):
    query = select(Faq)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_faq(session: AsyncSession, faq_id: int):
    query = select(Faq).where(Faq.id == faq_id)
    result = await session.execute(query)
    return result.scalar()



async def orm_delete_faq(session: AsyncSession, faq_id: int):
    query = delete(Faq).where(Faq.id == faq_id)
    await session.execute(query)
    await session.commit()

######################### add price ###############################################

async def orm_add_price(session: AsyncSession(), data: dict):
    obj = Price(
        name=data['name'],
        price=data['price'],
    )
    session.add(obj)
    await session.commit()


async def orm_get_prices(session: AsyncSession):
    query = select(Price)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_price(session: AsyncSession, price_id: int):
    query = delete(Price).where(Price.id == price_id)
    await session.execute(query)
    await session.commit()


######################### add document ###############################################

async def orm_add_document(session: AsyncSession(), data: dict):
    obj = Document(
        name=data['name'],
        document=data['document'],
    )
    session.add(obj)
    await session.commit()


async def orm_get_documents(session: AsyncSession):
    query = select(Document)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_document(session: AsyncSession, document_id: int):
    query = delete(Document).where(Document.id == document_id)
    await session.execute(query)
    await session.commit()


########################## add notes ###################################

async def orm_add_note(session: AsyncSession(), data: dict):
    obj = Notes(
        name=data['name'],
        description=data['description'],
    )
    session.add(obj)
    await session.commit()


async def orm_get_notes(session: AsyncSession):
    query = select(Notes)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_note(session: AsyncSession, note_id: int):
    query = select(Notes).where(Notes.id == note_id)
    result = await session.execute(query)
    return result.scalar()



async def orm_delete_note(session: AsyncSession, note_id: int):
    query = delete(Notes).where(Notes.id == note_id)
    await session.execute(query)
    await session.commit()
