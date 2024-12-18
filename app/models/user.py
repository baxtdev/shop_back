from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from app.db.session import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    products = relationship("Product", back_populates="user")
    password_hash = Column(String, nullable=False)
    orders = relationship("Order", back_populates="user")

    def set_password(self, password: str):
        """Устанавливает хэш пароля."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Проверяет пароль на совпадение с хэшом."""
        return pwd_context.verify(password, self.password_hash)
