from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from ashinity.core.db import Base

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)   # <-- FIXED
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)

    user = relationship("User", back_populates="inquiries")
    property = relationship("Property", back_populates="inquiries")