from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base  

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String,index=True) 
    phone = Column(String,index=True)
    user = relationship("User", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order")


class OrderProduct(Base):
    __tablename__ = "order_products"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")
    quantity = Column(Integer, default=0)
    