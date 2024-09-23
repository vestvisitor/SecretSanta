from src.api.deps import get_session
from sqlmodel import select
from sqlmodel import Session
import uuid
from fastapi import HTTPException, status

from src.api.routes.people.types import User as UserType
from src.api.routes.people.types import RegisterUser

from src.models import User as UserModel
from src.models import UserCreate as UserCreateModel


async def get_all_users(
        session: Session
) -> list[UserType]:
    users = session.exec(select(UserModel)).all()
    return users


async def get_user(
        session: Session,
        user_id: uuid.UUID
) -> UserType:
    user = session.exec(select(UserModel).where(UserModel.id == user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    return user


async def add_user_db(
        session: Session,
        user: RegisterUser
):
    return RegisterUser