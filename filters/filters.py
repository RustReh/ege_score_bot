import asyncio
from typing import List

from aiogram.filters import Filter
from aiogram import Bot, types
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database import user_registred_id_query


class RegisteredFilter(Filter):

    async def __call__(self, message: types.Message, bot: Bot, session: AsyncSession) -> bool:
        return message.from_user.id in await user_registred_id_query(session)
