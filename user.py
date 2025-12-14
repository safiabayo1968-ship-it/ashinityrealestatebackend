from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ashinity.core.db import Base
## from ashinity.models.user import User

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    properties = relationship("Property", back_populates="owner")
    inquiries = relationship("Inquiry", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
