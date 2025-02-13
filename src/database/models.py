from sqlalchemy import BigInteger, Text, Double
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Program(Base):
    __tablename__ = 'programs'
    id = mapped_column(BigInteger, primary_key=True, unique=True, index=True)
    title = mapped_column(Text)
    link = mapped_column(Text)
    price = mapped_column(Double, default=0)


class User(Base):
    __tablename__ = 'user'
    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username = mapped_column(Text)
    password = mapped_column(Text)
