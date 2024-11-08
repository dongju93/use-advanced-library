# from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from ..settings import Settings

# settings = get_settings()
# user_name = settings.database.user

# 사용 예시
settings = Settings()
user_name = settings.database.user


# user_name = get_secret("user", "database")

async_engine = create_async_engine(
    url=f"mariadb+asyncmy://{user_name}:password@127.0.0.1:3306/test-db",
    echo=True,
    pool_size=10,
)
