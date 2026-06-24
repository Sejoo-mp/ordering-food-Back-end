from fastapi import APIRouter, HTTPException, Depends
from models.menu import MenuItem
from utils.jwt import decode_token

router = APIRouter(prefix="/menu", tags=["Menu"])

def admin_required(user=Depends(decode_token)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden — admin only")
    return user

@router.get("/")
async def get_all_menu():
    return await MenuItem.find_all().to_list()

@router.get("/{id}")
async def get_menu_item(id: str):
    item = await MenuItem.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item