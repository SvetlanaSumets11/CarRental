from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserAuthSchema(BaseModel):
    email: str
    password: str


class UserSchema(UserBaseSchema):
    user_id: str
    password: str
    email_confirmed_at: datetime | None = None


class UserRegistrationSchema(UserBaseSchema):
    password: str
    user_id: str = Field(default_factory=lambda: str(uuid4()))


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
