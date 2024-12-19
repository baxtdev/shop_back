from pydantic import BaseModel
from typing import Optional

class CategoryFilter(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None     
