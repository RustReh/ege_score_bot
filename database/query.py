from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from bot.database.models import Students, Scores


async def register_query(session: AsyncSession, data: dict):
    obj = Students(
        id=data['id'],
        name=data["name"],
        surname=data["surname"],
    )
    session.add(obj)
    await session.commit()


async def login_query(session: AsyncSession,  student_id: int):
    query = update(Students).where(Students.id == student_id).values(
        status=True
    )
    await session.execute(query)
    await session.commit()


async def logout_query(session: AsyncSession, student_id: int):
    query = update(Students).where(Students.id == student_id).values(
        status=False
    )
    await session.execute(query)
    await session.commit()


async def add_score_query(session: AsyncSession, data: dict):
    obj = Scores(
        title=data["title"],
        score=data["score"],
        student_id=data["student_id"],
    )
    session.add(obj)
    await session.commit()


async def user_registred_id_query(session: AsyncSession):
    query = select(Students.id)
    result = await session.execute(query)
    return result.scalars().all()


async def view_student_score_query(session: AsyncSession, student_id: int):
    query = select(Scores).where(Scores.student_id == student_id)
    result = await session.execute(query)
    return result.scalars().all()
