from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List
from fastapi_pagination import Page, add_pagination, paginate


from app.db.session import get_db

from app.models.order import Order,OrderProduct
from app.models.user import User
from app.schemas.order import OrderBase, OrderUpdate, OrderOut,OrderCreate
from app.api.auth import get_current_user_from_token

router = APIRouter()

@router.get("/", response_model=Page[OrderOut])
async def get_orders(db: Session = Depends(get_db)):
    orders = ( 
        db.query(Order)
        .options(
            joinedload(Order.user),
            joinedload(Order.order_products).joinedload(OrderProduct.product)
        ).all()
    )
    return paginate(orders)


@router.get('/{order_id}',response_model=OrderOut)
def get_order(order_id:int,db:Session = Depends(get_db)):
    db_order = db.query(Order).options(joinedload(Order.user)).get(order_id)
    if db_order:
        return db_order
    raise HTTPException(status_code=404,detail=f"Order with id {order_id} does not found")


@router.post('/', response_model=OrderOut)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    print(current_user)
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"User with id {order_data.user_id} does not exist"
        )
    
    order = Order(user_id=order_data.user_id, name=order_data.name,phone=order_data.phone)  
    db.add(order)
    db.commit()
    db.refresh(order)
    
    order_products = []
    for product_data in order_data.order_products:
        order_product = OrderProduct(
            order_id=order.id, 
            product_id=product_data.product_id, 
            quantity=product_data.quantity
        )
        order_products.append(order_product)
    
    db.add_all(order_products)
    db.commit()

    db.refresh(order)
    
    return order


@router.delete('/{order_id}',status_code=204)
def delete_order(order_id:int,db:Session=Depends(get_db)):
    order = db.query(Order).get(order_id)
    db.delete(order)
    db.commit()
    return