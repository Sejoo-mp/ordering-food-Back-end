from fastapi import APIRouter, HTTPException
from schemas.auth import RegisterSchema, LoginSchema
from models.user import User
from utils.jwt import create_token
from utils.id_generator import get_next_id
import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

@router.post("/register")
async def register(data: RegisterSchema):
    existing_user = await User.find_one(User.email == data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    new_id = await get_next_id("user_id")
    hashed_password = hash_password(data.password)
    
    user = User(
        id=new_id,
        name=data.name,
        email=data.email,
        password=hashed_password,
        role=data.role
    )
    await user.insert()
    return {"message": "User registered", "id": new_id}

@router.post("/login")
async def login(data: LoginSchema):
    user = await User.find_one(User.email == data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong credentials")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong credentials")
    token = create_token({"id": user.id, "role": user.role})
    return {"token": token}

@router.get("/users")
async def get_all_users():
    return await User.find_all().to_list()