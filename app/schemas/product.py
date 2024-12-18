from pydantic import BaseModel
from typing import Optional
from .user import UserOut

class ProductBase(BaseModel):
    name: str
    quantity: int = 0
    viewers: int = 0
    user_id: int


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    viewers: Optional[int] = None
    user_id: Optional[int] = None


class ProductOut(ProductBase):
    id : int
    user: UserOut  

    class Config:
        orm_mode = True
