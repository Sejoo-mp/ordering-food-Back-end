from fastapi import APIRouter, HTTPException
from schemas.auth import RegisterSchema, LoginSchema
from models.user import User
from utils.jwt import create_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(data: RegisterSchema):
    existing_user = await User.find_one(User.email == data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")
    hashed_password = pwd_context.hash(data.password)
    user = User(
        name=data.name,
        email=data.email,
        password=hashed_password,
        role=data.role
    )
    await user.insert()
    return {"message": "User registered"}

@router.post("/login")
async def login(data: LoginSchema):
    user = await User.find_one(User.email == data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong credentials")
    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong credentials")
    token = create_token({"id": str(user.id), "role": user.role})
    return {"token": token}

@router.get("/users")
async def get_all_users():
    return await User.find_all().to_list()