from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.user import UserResponse,UserBase
from app.models.user import User
from app.schemas.token import Token
from app.core.security import create_access_token, verify_token
from app.api.deps import get_user_by_username,get_user_by_id,get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def get_current_user_from_token(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    print(token)
    try:
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = get_user_by_id(user_id,db)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired")




@router.post("/token", response_model=Token)
async def login_for_access_token(username: str, password: str,db:Session=Depends(get_db)):
    user = get_user_by_username(username,db) 
    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/profile/",response_model=UserResponse)
async def profile_read(token:str,db:Session=Depends(get_db)):
    current_user: User = get_current_user_from_token(token,db)
    return current_user


@router.put('/profile/',response_model=UserResponse)
async def profile_update(user_data:UserBase,token:str,db:Session=Depends(get_db)):
    current_user: User = get_current_user_from_token(token,db)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field,value in user_data.dict().items():   
        current_user.__setattr__(field,value)
    
    db.commit()
    db.refresh(current_user)
    return current_user