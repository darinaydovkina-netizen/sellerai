from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    generations_per_month = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"), nullable=False)
    generations_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product = Column(String(500), nullable=False)
    tools = Column(Text, nullable=False)
    marketplace = Column(String(100), nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        result = await session.execute(select(Tariff))
        if not result.scalars().first():
            session.add_all([
                Tariff(name="free", generations_per_month=5, price=0),
                Tariff(name="starter", generations_per_month=50, price=499),
                Tariff(name="business", generations_per_month=200, price=999),
                Tariff(name="pro", generations_per_month=-1, price=1990),
            ])
            await session.commit()
