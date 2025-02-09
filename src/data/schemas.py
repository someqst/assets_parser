from pydantic import BaseModel, Field
from enum import Enum


class ProgramSchema(BaseModel):
    id: int
    title: str
    link: str
    price: int = 0


class Range(str, Enum):
    free = "0...0"
    below_20 = "0.01...20"
    twenty_to_fifty = "20...50"
    fifty_to_hundred = "50...100"
    hundred_to_two_hundred = "100...200"


class UserSchema(BaseModel):
    username: str = Field(..., description="Имя пользователя")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")