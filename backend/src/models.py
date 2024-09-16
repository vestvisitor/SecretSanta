from sqlmodel import SQLModel, Field, Relationship
import uuid


class WishUserLink(SQLModel, table=True):
    wish_id: int | None = Field(default=None, foreign_key="wish.id", primary_key=True)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", primary_key=True)


class UserBase(SQLModel):
    username: str = Field(min_length=8, max_length=32)
    email: str = Field(max_length=254)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field()
    disabled: bool | None = None

    wishes: list["Wish"] = Relationship(back_populates="users", link_model=WishUserLink)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=25)


class UserPublic(UserBase):
    id: uuid.UUID


class UserLogin(SQLModel):
    username: str = Field(min_length=8, max_length=32)
    password: str = Field(min_length=8, max_length=25)


class WishMake(SQLModel):
    link: str
    priority: int = Field(default=1, ge=1, le=5)


class WishPars(SQLModel):
    name: str
    picture_src: str


class WishAdd(SQLModel):
    wish_id: int


class Wish(WishMake, WishPars, table=True):
    id: int | None = Field(default=None, primary_key=True)

    users: list[User] = Relationship(back_populates="wishes", link_model=WishUserLink)


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    sub: str | None = None
