from sys import modules

from fastapi import FastAPI, Depends
from sqlmodel import Session

from contextlib import asynccontextmanager

from .database import create_db_and_tables, drop_all_tables, get_session
from .models import *


def hash_password(password: str) -> str:
    return f"{password}secret"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await drop_all_tables()


app = FastAPI(lifespan=lifespan)


@app.post('/user/', response_model=UserPublic)
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


@app.get("/users/{user_id}", response_model=UserPublic)
async def read_user(
        *,
        session: Session = Depends(get_session),
        user_id: uuid.UUID
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
