import strawberry
from strawberry.types import Info

from src.api.routes.people.types import User, RegisterUser
from src.api.routes.people.resolvers import add_user_db


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def signup_user(self, info: Info, data: RegisterUser) -> User:
        session = info.context['session']
        return add_user_db(data, session)

