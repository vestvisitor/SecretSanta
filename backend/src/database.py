from sqlmodel import SQLModel, Session, create_engine
from .config import SQLITE_DB

db_address = f"sqlite:///{SQLITE_DB}.db"

engine = create_engine(
    db_address,
    echo= True
)

async def get_session():
    with Session(engine) as session:
        yield session


async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


async def drop_all_tables():
    SQLModel.metadata.drop_all(engine)

