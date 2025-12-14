from fastapi import APIRouter, Depends, HTTPException
## from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from ashinity.core.db import get_db
from ashinity.schemas.inquiry import InquiryCreate, InquiryOut
from ashinity.models.inquiry import Inquiry
from ashinity.models.property import Property
from ashinity.models.user import User
from ashinity.deps.auth import get_current_user

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])

@router.post("", response_model=InquiryOut, status_code=201)
async def create_inquiry(
    payload: InquiryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prop = db.execute(select(Property).where(Property.id == payload.property_id))
    if not prop.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Property not found")
    inquiry = Inquiry(user_id=current_user.id, property_id=payload.property_id, message=payload.message)
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry

@router.get("", response_model=list[InquiryOut])
def my_inquiries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = db.execute(select(Inquiry).where(Inquiry.user_id == current_user.id))
    return result.scalars().all()

@router.get("/property/{property_id}", response_model=list[InquiryOut])
async def inquiries_for_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prop = db.execute(select(Property).where(Property.id == property_id))
    p = prop.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Property not found")
    if p.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = db.execute(select(Inquiry).where(Inquiry.property_id == property_id))
    return result.scalars().all()
