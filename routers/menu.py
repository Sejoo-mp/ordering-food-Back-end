from fastapi import APIRouter, HTTPException
from models.menu import MenuItem

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/")
async def get_all_menu():
    return await MenuItem.find_all().to_list()

@router.get("/{id}")
async def get_menu_item(id: str):
    item = await MenuItem.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item