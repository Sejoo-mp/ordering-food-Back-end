from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routers.auth import router as auth_router
from routers.menu import router as menu_router
from routers.orders import router as orders_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(orders_router)

@app.get("/")
async def root():
    return {"message": "Food Ordering API"}