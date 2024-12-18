from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password : str
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True        


class Auth(BaseModel):
    password : str
    email : str