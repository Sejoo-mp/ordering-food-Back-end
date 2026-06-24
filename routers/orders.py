from fastapi import APIRouter, HTTPException, Depends
from models.order import Order
from models.menu import MenuItem
from schemas.orders import CreateOrderSchema, StatusSchema
from utils.jwt import decode_token

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
async def create_order(data: CreateOrderSchema, user=Depends(decode_token)):
    total_price = 0
    items = []
    for item in data.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")
        menu_item = await MenuItem.get(item.menu_item_id)
        if not menu_item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        if not menu_item.is_available:
            raise HTTPException(status_code=400, detail="Item unavailable")
        total_price += menu_item.price * item.quantity
        items.append({
            "menu_item_id": str(menu_item.id),
            "quantity": item.quantity,
            "price": menu_item.price
        })
    order = Order(user_id=user.get("id"), items=items, total_price=total_price)
    await order.insert()
    return order

@router.get("/my")
async def my_orders(user=Depends(decode_token)):
    return await Order.find(Order.user_id == user.get("id")).to_list()

@router.get("/")
async def all_orders(user=Depends(decode_token)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return await Order.find_all().to_list()

@router.patch("/{id}/status")
async def update_status(id: str, data: StatusSchema, user=Depends(decode_token)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    order = await Order.get(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = data.status
    await order.save()
    return order