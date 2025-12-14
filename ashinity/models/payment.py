from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ashinity.core.db import Base
## from ashinity.models.payment import Payment
from ashinity.models import User, Favorite, Property, Inquiry

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="NGN")
    method = Column(String, nullable=False)   # "paystack" or "flutterwave"
    status = Column(String, default="pending")  # "pending", "success", "failed"
    reference = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="payments")
