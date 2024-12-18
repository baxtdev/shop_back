from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List
from fastapi_pagination import Page, add_pagination, paginate


from app.db.session import get_db
from app.schemas.blog import CategoryBase,NewsBase,CategoryOut,NewsOut
from app.models.blog import Category,News
router = APIRouter()


@router.get('/categories/',response_model=Page[CategoryOut])
def list_catgeory(db:Session = Depends(get_db)):
    db_query = db.query(Category).all()
    return paginate(db_query)

@router.get('/categories/{id}',response_model=CategoryOut)
def read_category(id:int,db:Session= Depends(get_db)):
    db_query = db.query(Category).filter(Category.id==id).first()
    if not db_query:
        raise HTTPException(status_code=404,detail=f"Category with id {id} does not founded")
    return db_query


@router.post('/categories/',response_model=CategoryOut)
def create_category(category_data:CategoryBase,db:Session = Depends(get_db)):
    category = Category(**category_data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put('/categories/{id}',response_model=CategoryOut)
def update_category(id:int,category_data:CategoryBase,db:Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id==id).first()
    if not category:
        raise HTTPException(status_code=404,detail=f"Ctageor with id {id} does not founded")
    for key,value in category_data.dict().items():
        category.__setattr__(key,value)

    db.commit()
    db.refresh(category)  
    return category  


@router.delete("/categories/{id}", status_code=204)
def delete_product(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(category)
    db.commit()
    return


@router.get('/news/',response_model=Page[NewsOut])
def get_list_news(db:Session = Depends(get_db)):
    db_query = db.query(News).options(joinedload(News.category)).all()
    return paginate(db_query)


@router.get('/news/{id}',response_model=NewsOut)
def get_news(id:int,db:Session = Depends(get_db)):
    news = db.query(News).options(joinedload(News.category)).get(id)
    if not news:
        raise HTTPException(status_code=404,detail=f"News with id {id} ddoes not found")
    
    return news


@router.post('/news/',response_model=NewsBase)
def create_news(news_data:NewsBase,db:Session = Depends(get_db)):
    category = db.query(Category).get(news_data.category_id)
    if not category:
        raise HTTPException(status_code=400,detail=f"Catehgory with id {news_data.category_id} does not exist")
    news = News(**news_data.dict())
    db.add(news)
    db.commit()
    db.refresh(news)
    return news
    



    