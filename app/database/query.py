from typing import Literal

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .connector import async_engine
from .model.table import User


async def get_user_row(idx: int):
    # sqlalchemy 의 비동기 session 사용
    async with AsyncSession(async_engine) as session:
        # sqlmodel 의 select 사용
        statement = select(User).where(User.idx == idx)
        """
        session 이 bind 된 async_engine은 asyncmy 를 사용해 생성
        session 이 비동기로 동작하므로 await 사용
        """
        result = await session.exec(statement)
        # sqlmodel 의 first 함수 사용
        user = result.first()
        return user


async def create_user_row(user: User) -> Literal["User created successfully"]:
    try:
        async with AsyncSession(async_engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
    except Exception as e:
        raise e
    else:
        return "User created successfully"
