from pydantic import BaseModel

class PaymentCreate(BaseModel):
    amount: float
    currency: str = "NGN"
    method: str
    email: str

class PaymentOut(BaseModel):
    id: int
    amount: float
    currency: str
    method: str
    status: str
    reference: str

    class Config:
        orm_mode = True
