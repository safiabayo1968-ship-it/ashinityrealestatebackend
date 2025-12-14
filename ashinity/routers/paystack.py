import requests, uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ashinity.core.db import get_db
from ashinity.models import Payment
from ashinity.schemas.payment import PaymentCreate, PaymentOut

router = APIRouter(prefix="/paystack", tags=["payments"])

PAYSTACK_SECRET_KEY = "sk_test_xxx"  # replace with your secret key

@router.post("/initiate", response_model=PaymentOut)
def initiate_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    data = {"email": payment.email, "amount": int(payment.amount * 100)}  # amount in kobo
    response = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Payment initiation failed")

    result = response.json()
    new_payment = Payment(
        user_id=1,  # replace with actual logged-in user
        amount=payment.amount,
        currency=payment.currency,
        method="paystack",
        reference=result["data"]["reference"],
        status="pending"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/verify/{reference}", response_model=PaymentOut)
def verify_payment(reference: str, db: Session = Depends(get_db)):
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Verification failed")

    result = response.json()
    payment = db.query(Payment).filter(Payment.reference == reference).first()
    if payment:
        payment.status = "success" if result["data"]["status"] == "success" else "failed"
        db.commit()
        db.refresh(payment)
    return payment
