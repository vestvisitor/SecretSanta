from pwd import struct_passwd
from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
import uuid
from src.models import UserPublic, UserCreate, User, Token, UserLogin
from src.api.deps import SessionDep, authenticate_user, CurrentActiveUser

from fastapi.security import OAuth2PasswordRequestForm

from src.core.security import get_password_hash, create_access_token
from src.core.config import settings

router = APIRouter(
    prefix="/users"
)


@router.get("/me", response_model=UserPublic)
async def read_me(
        current_user: CurrentActiveUser,
):
    """
        Fetches data about current user;
        Also used for user authentication from frontend;

        Args:
            current_user (dependency):
                Headers {
                'Authorization': `Bearer ${token}`
                }, where token is JWT token;

        Returns:
            An instance of UserPublic class with id, username, email attributes;

        Raises:
            HTTP_401_UNAUTHORIZED, if current user is not authorized;
            HTTP_404_NOT_FOUND, if current user is disabled;
    """

    return current_user


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(
        *,
        current_user: CurrentActiveUser,
        session: SessionDep,
        user_id: uuid.UUID
):

    """
        Fetches data about a particular user by his id;

        Args:
            current_user (dependency):
                Headers {
                'Authorization': `Bearer ${token}`
                }, where token is JWT token;
            session (dependency): an instance of database connection;
            user_id: uuid, selected user's id;

        Returns:
            An instance of UserPublic class with id, username, email attributes

        Raises:
            HTTP_401_UNAUTHORIZED, if current_user is not authorized;
            HTTP_404_NOT_FOUND, if current_user is disabled;
    """

    user = session.exec(select(User).where(User.id == user_id)).first()

    return user


@router.post("/signup", response_model=UserPublic)
async def signup_user(
        *,
        session: SessionDep,
        user: UserCreate
):

    """
        Creates user account;

        Args:
            session (dependency): an instance of database connection;
            user: an instance of UserCreate class with username, email, password attributes;

        Returns:
            An instance of UserPublic class with id, username, email attributes;

        Raises:
            HTTP_409_CONFLICT, if username or email is already in database;
    """

    username_db = session.exec(select(User).where(User.email == user.email)).first()
    if username_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with such username already exists"
        )

    email_db = session.exec(select(User).where(User.email == user.email)).first()
    if email_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with such email already exists"
        )

    hashed_password = get_password_hash(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.post("/token", response_model=Token)
async def login_user(
        *,
        session: SessionDep,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
        Authenticates user and creates access token;

        Args:
            session (dependency): an instance of database connection;
            form_data (dependency): OAuth2PasswordRequestForm with required username and password fields;

        Returns:
            An instance of Token class with access_token and token_type attributes;

        Raises:
            HTTP_401_UNAUTHORIZED, username is not in database | wrong password;
    """

    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
