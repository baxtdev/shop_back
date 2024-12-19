from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page, add_pagination, paginate
from typing import List
from fastapi_permissions import ( Allow,
    Authenticated,
    Deny,
    Everyone,
    configure_permissions,
    list_permissions)

from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.models.user import User



router = APIRouter()

@router.get("/", response_model=Page[ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).options(joinedload(Product.user)).all()
    return paginate(products)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).options(joinedload(Product.user)).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductOut)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
    ):
    user = db.query(User).filter(User.id == product_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"User with id {product_data.user_id} does not exist"
        )
    
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    user = db.query(User).filter(User.id == product_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"User with id {product_data.user_id} does not exist"
        )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return

