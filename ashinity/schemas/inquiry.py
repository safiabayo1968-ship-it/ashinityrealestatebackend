from pydantic import BaseModel

class InquiryCreate(BaseModel):
    property_id: int
    message: str

class InquiryOut(BaseModel):
    id: int
    property_id: int
    user_id: int
    message: str

    model_config = {"from_attributes": True}
