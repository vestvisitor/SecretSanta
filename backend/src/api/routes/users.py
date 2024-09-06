from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import uuid
from src.models import UserPublic, UserCreate, User
from src.database import get_session

router = APIRouter(
    prefix="/users"
)


def hash_password(password: str) -> str:
    return f"{password}secret"


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(
        *,
        session: Session = Depends(get_session),
        user_id: uuid.UUID
    ):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=UserPublic)
async def create_user(
        *,
        session: Session = Depends(get_session),
        user: UserCreate
):
    hashed_password = hash_password(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
