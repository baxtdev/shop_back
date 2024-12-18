from pydantic import BaseModel
from typing import Optional,List
from .user import UserOut
from .product import ProductOut

class OrderBase(BaseModel):
    name: str
    phone: str
    user_id: int


class OrderUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    user_id: Optional[int] = None
    
    class Config:
        orm_mode = True


class OrderProductBase(BaseModel):
    product_id : int
    quantity : int


class OrderProductOut(OrderProductBase):
    id : int
    product : ProductOut


class OrderOut(OrderBase):
    id : int
    user: UserOut
    order_products : List[OrderProductOut]
    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    order_products : List[OrderProductBase]
    class Config:
        orm_mode = True
