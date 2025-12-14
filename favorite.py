from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ashinity.core.db import Base

class Favorite(Base):
      
     __tablename__ = "favorites"  

     id = Column(Integer, primary_key=True, index=True)   # <-- REQUIRED
     user_id = Column(Integer, ForeignKey("users.id"))
     property_id = Column(Integer, ForeignKey("properties.id"))     


     user = relationship("User", back_populates="favorites")
     property = relationship("Property", back_populates="favorites")
