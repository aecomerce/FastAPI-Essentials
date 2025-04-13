from pydantic import BaseModel


class UserFeedback(BaseModel):
    name: str
    message: str
