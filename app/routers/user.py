from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate

from app.schemas.user import UserCreate, UserResponse,Auth
from app.models.user import User
from app.db.session import SessionLocal,get_db

router = APIRouter()



@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=Page[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return paginate(users)


@router.get('/{id}',response_model=UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

@router.put('/{id}',response_model=UserResponse)
def update_user(id:int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field,value in user.dict().items():   
        db_user.__setattr__(field,value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete('/{id}')
def delete_user(id:int, db: Session = Depends(get_db)):
    db_user = db.query(User).get(id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()

    return JSONResponse(content={"detail": f"User with id {id} deleted "})


@router.post('/login',response_model=UserResponse)
def auth_user(auth:Auth,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email==auth.email).first()
    
    if user and user.verify_password(auth.password):
        return user
    
    raise HTTPException(status_code=400,detail="Invalid email or password")
    

