from sqlalchemy import Column, String, Text, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ashinity.core.db import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False, default=1)
    bathrooms = Column(Integer, nullable=False, default=1)
    area_sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="properties")
    inquiries = relationship("Inquiry", back_populates="property", cascade="all,delete")
    favorites = relationship("Favorite", back_populates="property", cascade="all,delete")
