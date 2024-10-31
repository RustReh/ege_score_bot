from typing import Any

from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column



class Base(DeclarativeBase):
    id: Any
    __name__ = str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class Students(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    surname: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True)

class Scores(Base):
    __tablename__ = 'scores'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'), nullable=False)


