from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
