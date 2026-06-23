from fastapi import APIRouter, HTTPException
from schemas.auth import RegisterSchema
from models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(data: RegisterSchema):
    existing_user = await User.find_one(User.email == data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")
    user = User(**data.dict())
    await user.insert()
    return {"message": "User registered"}