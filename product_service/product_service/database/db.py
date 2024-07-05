
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends
from product_service import settings
from contextlib import asynccontextmanager 


connection_string = str(settings.DB_URL).replace(
    "postgresql", "postgresql+psycopg")

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield


def get_session():
    with Session(engine) as session:
        yield session