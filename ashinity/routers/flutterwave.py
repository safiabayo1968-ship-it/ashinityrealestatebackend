import requests, uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ashinity.core.db import get_db
from ashinity.schemas.payment import PaymentCreate, PaymentOut
from ashinity.models import Payment

router = APIRouter(prefix="/flutterwave", tags=["payments"])

FLUTTERWAVE_SECRET_KEY = "FLWSECK_TEST-xxx"  # replace with your secret key

@router.post("/initiate", response_model=PaymentOut)
def initiate_flutterwave(payment: PaymentCreate, db: Session = Depends(get_db)):
    headers = {"Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}"}
    tx_ref = str(uuid.uuid4())
    data = {
        "tx_ref": tx_ref,
        "amount": payment.amount,
        "currency": payment.currency,
        "redirect_url": "http://localhost:3000/payment/callback",
        "customer": {"email": payment.email}
    }
    response = requests.post("https://api.flutterwave.com/v3/payments", json=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Payment initiation failed")

    result = response.json()
    new_payment = Payment(
        user_id=1,
        amount=payment.amount,
        currency=payment.currency,
        method="flutterwave",
        reference=tx_ref,
        status="pending"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/verify/{tx_ref}", response_model=PaymentOut)
def verify_flutterwave(tx_ref: str, db: Session = Depends(get_db)):
    headers = {"Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}"}
    response = requests.get(f"https://api.flutterwave.com/v3/transactions/{tx_ref}/verify", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Verification failed")

    result = response.json()
    payment = db.query(Payment).filter(Payment.reference == tx_ref).first()
    if payment:
        payment.status = "success" if result["data"]["status"] == "successful" else "failed"
        db.commit()
        db.refresh(payment)
    return payment
