from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base




class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)  
    news = relationship("News", back_populates="category", cascade="all, delete-orphan") 


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)  
    description = Column(String(1000), nullable=True, index=True) 
    photo = Column(String(500), nullable=True)  
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))  
    category = relationship("Category", back_populates="news")
    