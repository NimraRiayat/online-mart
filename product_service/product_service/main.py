from typing import  Optional, Annotated
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends, HTTPException
from product_service.models.products import Products, ProductDelete, ProductCreate, ProductUpdate
from product_service.database.db import get_session, lifespan
from product_service import settings
from contextlib import asynccontextmanager    



# connection_string = str(settings.DB_URL).replace(
#     "postgresql", "postgresql+psycopg")

# engine = create_engine(
#     connection_string, connect_args={}, pool_recycle=300)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Creating tables..")
#     create_db_and_tables()
#     yield

app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8000", 
            "description": "Development Server"
        }
        ])

# def get_session():
#     with Session(engine) as session:
#         yield session

@app.get("/")
def read_root():
    return {"message" : "Product service"}

@app.post("/product-servive/", response_model=ProductCreate)
def create_product(todo: ProductCreate, session: Annotated[Session, Depends(get_session)]):
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.get("/product-servive/", response_model=list[Products])
def read_product(session: Annotated[Session, Depends(get_session)]):
        products = session.exec(select(Products)).all()
        return products

@app.put("/product-servive/{product_id}/", response_model=ProductCreate)
def update_product( product_id: int, todo: ProductCreate, session: Annotated[Session, Depends(get_session)]):
    db_product = session.get(Products, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    for key, value in todo.dict().items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.delete("/product-servive/{product_id}/", response_model=ProductCreate)
def delete_product(
    product_id: int, session: Annotated[Session, Depends(get_session)]
):
    db_product = session.get(Products, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    session.delete(db_product)
    session.commit()
    return db_product