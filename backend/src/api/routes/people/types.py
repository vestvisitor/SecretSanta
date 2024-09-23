import strawberry
import uuid


@strawberry.type
class User:
    id: uuid.UUID
    username: str
    email: str


@strawberry.type
class RegisterUser:
    username: str
    email: str
    password: str
