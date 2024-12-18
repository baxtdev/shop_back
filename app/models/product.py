from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base  


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)
    viewers = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id")) 

    user = relationship("User", back_populates="products")
    order_products = relationship("OrderProduct", back_populates="product")  # Связь с OrderProduct

