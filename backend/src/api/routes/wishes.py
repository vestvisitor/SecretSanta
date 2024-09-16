import uuid
from math import ceil
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session, select

from src.api.deps import SessionDep, CurrentActiveUser

from src.models import WishMake, Wish, User, WishAdd, WishUserLink

from src.parser.main import parse_item_info


router = APIRouter(
    prefix="/wishes"
)


@router.get("", response_model=list[Wish])
async def get_wishes(
        *,
        session: SessionDep,
        offset: int | None = 0,
        limit: int | None = Query(default=5, le=5)
):
    """
        Fetches all wishes for the home page in frontend;

        Args:
            session (dependency): an instance of database connection;
            offset: int | None = 0, used for skipping n-number of rows;
            limit: int | None = 5 (less or equal to 5), used to limit receiving data per request;

        Returns:
            List of instances of Wish class;

        Raises:
            HTTP_422_UNPROCESSABLE_ENTITY, incorrect query parameters;
    """

    result = session.exec(select(Wish).offset(offset).limit(limit)).all()
    result.reverse()

    return result


@router.get("/public-pagination", response_model=int)
async def get_pages_count_public(
        session: SessionDep
):
    """
        Calculates pagination for all wishes at the home page in frontend;

        Args:
            session (dependency): an instance of database connection;

        Returns:
            Integer, number of pages;
    """

    result = len(session.exec(select(Wish.id)).all())
    pages = ceil(result/5) * 10

    return pages


@router.get("/{user_id}", response_model=list[Wish])
async def get_user_wishlist(
        *,
        session: SessionDep,
        user_id: uuid.UUID,
        offset: int | None = 0,
        limit: int | None = Query(default=5, le=5)
):
    """
        Fetches all wishes of a particular user by his id;

        Args:
            session (dependency): an instance of database connection;
            user_id: uuid, selected user's id;
            offset: int | None = 0, used for skipping n-number of rows;
            limit: int | None = 5 (less or equal to 5), used to limit receiving data per request;

        Returns:
            List of instances of Wish class;

        Raises:
            HTTP_422_UNPROCESSABLE_ENTITY, incorrect query parameters;
    """

    statement = select(Wish).join(WishUserLink).where(WishUserLink.user_id == user_id).offset(offset).limit(limit)
    result = session.exec(statement).all()
    result.reverse()
    return result


@router.get("/private-pagination/{user_id}", response_model=int)
async def get_pages_count_private(
        *,
        session: SessionDep,
        user_id: uuid.UUID
):
    """
        Calculates pagination for all wishes of a particular user;

        Args:
            session (dependency): an instance of database connection;
            user_id: uuid, selected user's id;

        Returns:
            Integer, number of pages;
    """

    result = len(session.exec(select(WishUserLink.wish_id).where(WishUserLink.user_id == user_id)).all())

    pages = ceil(result/5) * 10

    return pages


@router.post("/share", response_model=str)
async def share_users_wishlist(
        current_user: CurrentActiveUser
):
    """
        Generates a link for sharing user's wishlist;

        Args:
            current_user (dependency):
                Headers {
                'Authorization': `Bearer ${token}`
                }, where token is JWT token;

        Returns:
            String, link to user's wishlist;
    """

    link = f"http://localhost:5173/#wishlist/{current_user.id}"

    return link


@router.post("/add", response_model=bool)
async def add_wish(
        *,
        current_user: CurrentActiveUser,
        session: SessionDep,
        wish: WishAdd
):
    """
        Adds a particular wish to a user's wishlist;

        Args:
            current_user (dependency):
                Headers {
                'Authorization': `Bearer ${token}`
                }, where token is JWT token;
            session (dependency): an instance of database connection;
            wish: an instance of WishAdd class with wish_id attribute;

        Returns:
            bool, True if succeeded;

        Raises:
            HTTP_409_CONFLICT, wish already in user's wishlist;
    """

    statement = select(Wish.id).join(WishUserLink).where(WishUserLink.user_id == current_user.id)
    user_wishlist = session.exec(statement).all()

    if wish.wish_id in user_wishlist:
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="You already have this wish in your wishlist"
                )

    user = session.exec(select(User).where(User.id == current_user.id)).first()
    db_wish = session.exec(select(Wish).where(Wish.id == wish.wish_id)).first()

    user.wishes.append(db_wish)
    session.commit()
    session.refresh(db_wish)

    return True


@router.post("/make")
async def make_wish(
        *,
        current_user: CurrentActiveUser,
        session: SessionDep,
        wish: WishMake
):
    """
        Creates a new wish by parsing its data via presented link and adds it to user's wishlist;

        Args:
            current_user (dependency):
                Headers {
                'Authorization': `Bearer ${token}`
                }, where token is JWT token;
            session (dependency): an instance of database connection;
            wish: an instance of WishMake class with link and priority attributes;

        Returns:
            HTTP_201_CREATED, wish successfully created;

        Raises:
            HTTP_503_SERVICE_UNAVAILABLE, marketplaces updated their websites;
    """

    user = session.exec(select(User).where(User.id == current_user.id)).first()

    wish_in_db = session.exec(select(Wish).where(Wish.link == wish.link)).first()

    if wish_in_db:
        user.wishes.append(wish_in_db)
        session.add(user)
        session.commit()
        return status.HTTP_200_OK

    try:
        result = parse_item_info(wish.link)
        extra_data = {
            "name": result.name,
            "picture_src": result.picture_src,
        }

        db_wish = Wish.model_validate(wish, update=extra_data)
        session.add(db_wish)

        user.wishes.append(db_wish)
        session.add(user)

        session.commit()
        return status.HTTP_201_CREATED
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is temporary unavailable"
        )


@router.delete("/delete", response_model=bool)
async def delete_wish(
        *,
        current_user: CurrentActiveUser,
        session: SessionDep,
        wish_id: int
):
    """
        Deletes selected wish in user's wishlist

        Args:
            current_user (dependency):
                Headers {
                'Authorization': `Bearer ${token}`
                }, where token is JWT token;
            session (dependency): an instance of database connection;
            wish_id: int, and id of a wish to delete;

        Returns:
            bool, wish successfully deleted;

        Raises:
            HTTP_404_NOT_FOUND, wish was not found;
    """

    wish = session.get(Wish, wish_id)
    if not wish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish not found"
        )

    user = session.exec(select(User).where(User.id == current_user.id)).first()
    user.wishes.remove(wish)
    session.commit()

    return True
