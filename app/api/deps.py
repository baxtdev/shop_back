from fastapi import Depends, HTTPException, Request,status
from app.core.security import verify_token
from sqlalchemy.orm import Session

from app.models.user import User
from app.db.session import get_db




def get_user_by_id(user_id: int, db: Session=Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(username:str,db:Session=Depends(get_db)):
    return db.query(User).filter(User.email==username).first()
