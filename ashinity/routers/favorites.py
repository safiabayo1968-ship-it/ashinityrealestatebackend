from fastapi import APIRouter, Depends, HTTPException
## from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from ashinity.core.db import get_db
from ashinity.models import Favorite
from ashinity.models.property import Property
from ashinity.models.user import User
from ashinity.deps.auth import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{property_id}", status_code=201)
def add_favorite(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prop =  db.execute(select(Property).where(Property.id == property_id))
    if not prop.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Property not found")
    exists = db.execute(
        select(Favorite).where(Favorite.user_id == current_user.id, Favorite.property_id == property_id)
    )
    if exists.scalar_one_or_none():
        return {"detail": "Already favorited"}
    fav = Favorite(user_id=current_user.id, property_id=property_id)
    db.add(fav)
    db.commit()
    return {"detail": "Added to favorites"}

@router.get("", response_model=list[int])
async def list_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Favorite).where(Favorite.user_id == current_user.id))
    return [f.property_id for f in result.scalars().all()]

@router.delete("/{property_id}", status_code=204)
async def remove_favorite(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = db.execute(
        select(Favorite).where(Favorite.user_id == current_user.id, Favorite.property_id == property_id)
    )
    fav = result.scalar_one_or_none()
    if not fav:
        return
    db.delete(fav)
    db.commit()
