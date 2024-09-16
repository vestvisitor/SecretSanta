from sqlmodel import SQLModel, Session, create_engine

from src.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    # echo= True,
    connect_args={"check_same_thread": False}
)


async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


async def drop_all_tables():
    SQLModel.metadata.drop_all(engine)
