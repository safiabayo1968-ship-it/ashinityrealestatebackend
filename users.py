from fastapi import APIRouter, Depends
from ashinity.deps.auth import get_current_user
from ashinity.models.user import User
from ashinity.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
