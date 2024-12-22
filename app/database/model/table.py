from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    idx: int = Field(primary_key=True)
    first_name: str
    last_name: str
    email: EmailStr = Field(unique=True)
    user_id: str = Field(unique=True)
    password: str
    address: str
    created_at: datetime = Field(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
    updated_at: datetime = Field(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
    suspend: bool = Field(default=False)
