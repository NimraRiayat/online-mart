from typing import  Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel



class Products(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    #price, description, created_at, updated_at

class ProductCreate(BaseModel):
    name: str 
    
class ProductUpdate(ProductCreate):
    pass     

class ProductDelete(ProductCreate):
    pass   