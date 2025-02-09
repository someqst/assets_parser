from sqlalchemy import select
from data.config import settings
from database.models import Program, User
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


engine = create_async_engine(url=settings.DB_URI.get_secret_value())
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class ProgramRepository:
    @classmethod
    async def add_all_progs(cls, prgorams: dict, session: AsyncSession):
        for result in prgorams['results']:
            id = int(str(result['clickUri']).split('/')[-1])
            session.add(Program(id = id, title = result['title'], link = result['clickUri'], price = int(result['raw']['ec_price'])))
        await session.commit()


    @classmethod
    async def filter_progs(cls, from_, to, session: AsyncSession) -> list[Program] | list[None]:
        return (await session.execute(select(Program).filter((Program.price >= from_) & (Program.price <= to)))).scalars().all()
    

    @classmethod
    async def select_asset_by_id(cls, asset_id, session: AsyncSession) -> Program | None:
        return (await session.execute(select(Program).where(Program.id == asset_id))).scalar_one_or_none()
    

class UserRepository:
    @classmethod
    async def register_user(cls, username, password, session: AsyncSession):
        session.add(User(username = username, password = password))
        await session.commit()

    @classmethod
    async def get_user_from_db(cls, username, session: AsyncSession) -> User | None:
        return (await session.execute(select(User).where(User.username == username))).scalar_one_or_none()