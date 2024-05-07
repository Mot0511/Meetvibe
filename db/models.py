from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    age: Mapped[int] = mapped_column(Numeric(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str] = mapped_column(String(150), nullable=False)
    location: Mapped[str] = mapped_column(String(150))
    school: Mapped[str] = mapped_column(String(150))
    hobbies: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(150))
    photo: Mapped[str] = mapped_column(String(150), nullable=False)

# class Stats(Base):
#     __tabelname__ = 'stats'
    
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
