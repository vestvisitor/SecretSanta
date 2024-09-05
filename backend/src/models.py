from sqlmodel import SQLModel, Field, Relationship
import uuid


class UserBase(SQLModel):
    first_name: str
    last_name: str


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field()


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: uuid.UUID


class WishBase(SQLModel):
    name: str
    link: str
    priority: int

    creator_id: uuid.UUID = Field(foreign_key="user.id")


class Wish(WishBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class WishlistBase(SQLModel):
    name: str
    owner_id: uuid.UUID = Field(foreign_key="user.id")


class Wishlist(WishlistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class WishlistPublic(WishlistBase):
    wishes: list[WishBase]


# class Game(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#
#     creator: uuid.UUID = Field(foreign_key="user.id")
#     participants: ["User"]
