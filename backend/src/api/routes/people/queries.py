import uuid
import strawberry
from strawberry.types import Info

from src.api.routes.people.types import User
from src.api.routes.people.resolvers import get_all_users, get_user


@strawberry.type
class UserQuery:
    @strawberry.field
    async def users(self, info: Info) -> list[User]:
        session = info.context['session']
        return await get_all_users(session)

    @strawberry.field
    async def user(self, info: Info, user_id: uuid.UUID) -> User:
        session = info.context['session']
        return await get_user(session, user_id)
