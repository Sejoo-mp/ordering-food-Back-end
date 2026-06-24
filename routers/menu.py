from fastapi import APIRouter, HTTPException, Depends
from models.menu import MenuItem
from schemas.menu import MenuCreate, MenuUpdate
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

@router.post("/", dependencies=[Depends(admin_required)])
async def create_menu(data: MenuCreate):
    item = MenuItem(**data.dict())
    await item.insert()
    return item

@router.put("/{id}", dependencies=[Depends(admin_required)])
async def update_menu(id: str, data: MenuUpdate):
    item = await MenuItem.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in data.dict().items():
        setattr(item, key, value)
    await item.save()
    return item

@router.delete("/{id}", dependencies=[Depends(admin_required)])
async def delete_menu(id: str):
    item = await MenuItem.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()
    return {"message": "Deleted"}