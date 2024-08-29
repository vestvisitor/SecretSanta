from sqlmodel import SQLModel, Field, Relationship
import uuid


class UserBase(SQLModel):
    first_name: str
    second_name: str


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: uuid.UUID


class Gift(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    link: str

    creator: uuid.UUID = Field(foreign_key="user.id")
