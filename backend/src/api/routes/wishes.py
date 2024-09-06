from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from src.database import get_session
from src.models import WishBase, Wish
import uuid

router = APIRouter(
    prefix="/wishes"
)


@router.get("")
async def get_wishes(
        *,
        session: Session = Depends(get_session),
        offset: int | None = 0,
        limit: int | None = Query(default=10, le=10)
    ):
    result = session.exec(select(Wish).offset(offset).limit(limit)).all()
    return result


@router.get("/wishes/{user_id}")
async def get_user_wishes(
        *,
        session: Session = Depends(get_session),
        user_id: uuid.UUID,
        offset: int | None = 0,
        limit: int | None = Query(default=10, le=10)
    ):
    result = session.exec(select(Wish).where(Wish.creator_id == user_id).offset(offset).limit(limit)).all()
    return result


@router.post("/wish/")
async def make_wish(
        *,
        session: Session = Depends(get_session),
        wish: WishBase
    ):
    db_wish = Wish.model_validate(wish)
    session.add(db_wish)
    session.commit()
    session.refresh(db_wish)
    return db_wish
