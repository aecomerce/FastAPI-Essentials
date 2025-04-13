from pydantic import BaseModel, EmailStr


class Data(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None
    is_subscribed: bool | None = None
