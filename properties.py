from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
## from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ashinity.core.db import get_db
from ashinity.schemas.property import PropertyCreate, PropertyUpdate, PropertyOut
from ashinity.models.property import Property
from ashinity.models.user import User
from ashinity.deps.auth import get_current_user

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("", response_model=list[PropertyOut])
def list_properties(
    db: Session = Depends(get_db),
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    bedrooms: int | None = None,
    bathrooms: int | None = None,
    published: bool | None = True,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    filters = []
    if city: filters.append(Property.city.ilike(f"%{city}%"))
    if state: filters.append(Property.state.ilike(f"%{state}%"))
    if country: filters.append(Property.country.ilike(f"%{country}%"))
    if min_price is not None: filters.append(Property.price >= min_price)
    if max_price is not None: filters.append(Property.price <= max_price)
    if bedrooms is not None: filters.append(Property.bedrooms >= bedrooms)
    if bathrooms is not None: filters.append(Property.bathrooms >= bathrooms)
    if published is not None: filters.append(Property.is_published == published)

    stmt = select(Property).where(and_(*filters)) if filters else select(Property)
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = db.execute(stmt)
    items = result.scalars().all()
    return items

@router.get("/{property_id}", response_model=PropertyOut)
def get_property(property_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Property).where(Property.id == property_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    return item

@router.post("", response_model=PropertyOut, status_code=201)
def create_property(
    payload: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prop = Property(owner_id=current_user.id, **payload.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

@router.patch("/{property_id}", response_model=PropertyOut)
def update_property(
    property_id: int,
    payload: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = db.execute(select(Property).where(Property.id == property_id))
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    if prop.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(prop, k, v)
    db.commit()
    db.refresh(prop)
    return prop

@router.delete("/{property_id}", status_code=204)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = db.execute(select(Property).where(Property.id == property_id))
    prop = result.scalar_one_or_none()
    if not prop:
        return
    if prop.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(prop)
    db.commit()
