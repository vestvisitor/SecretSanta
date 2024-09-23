from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types
from strawberry import Schema
from fastapi import Request
from sqlmodel import Session

from src.api.deps import SessionDep

from src.api.routes.people.queries import UserQuery

# queries = UserQuery
# mutations = (UserMutation, TeamMutation)

# Query = merge_types('Query', queries)
# Mutation = merge_types('Mutation', mutations)

async def get_context(request: Request, session: SessionDep):
    return {
        'session': session,
    }

schema = Schema(query=UserQuery)

router = GraphQLRouter(
    prefix="/graphql",
    schema=schema,
    context_getter=get_context
)
