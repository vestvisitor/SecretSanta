from sys import modules

from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select

from contextlib import asynccontextmanager

from .database import create_db_and_tables, drop_all_tables, get_session
from .models import *
import uuid

from src.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await drop_all_tables()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
