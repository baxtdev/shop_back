from pydantic import BaseModel
from typing import Optional,List

class CategoryBase(BaseModel):
    name : str

class CategoryOut(CategoryBase):
    id : int

    

class NewsBase(BaseModel):
    name : str
    description : str
    photo : str
    category_id : int    


class NewsOut(NewsBase):
    id : int
    category : CategoryOut

    class Config:
        orm_mode = True