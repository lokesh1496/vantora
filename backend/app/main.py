from fastapi import FastAPI

from app.routes.product import router as product_router
from app.routes.category import router as category_router
from app.routes.supplier import router as supplier_router
from app.routes.purchase import router as purchase_router
from app.routes.stock_movement import router as inventory_router


app = FastAPI(
    title="Vantora API",
    description="Supermarket Inventory Management System",
    version="1.0.0"
)


app.include_router(product_router)
app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(purchase_router)
app.include_router(inventory_router)


@app.get("/")
def root():
    return {
        "message": "Vantora API is running"
    }