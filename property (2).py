from pydantic import BaseModel
from typing import Optional

class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    country: str
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: Optional[int] = None
    is_published: bool = True

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[int] = None
    is_published: Optional[bool] = None

class PropertyOut(PropertyBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}
