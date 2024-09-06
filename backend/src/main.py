from fastapi import FastAPI

from contextlib import asynccontextmanager

from .database import create_db_and_tables, drop_all_tables

from src.api.main import api_router

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await drop_all_tables()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
