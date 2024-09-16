from sqlmodel import Session, select
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
import jwt

from src.core.db import engine
from src.core.config import settings
from src.core.security import ALGORITHM, verify_password

from src.models import User, UserPublic, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


async def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(
        session: SessionDep,
        token: TokenDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(sub=username)
    except InvalidTokenError:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == token_data.sub)).first()
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(
    current_user: CurrentUser
) -> UserPublic:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inactive user")
    user = UserPublic.model_validate(current_user)
    return user


CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]


async def authenticate_user(
        username: str,
        password: str,
        session
):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
