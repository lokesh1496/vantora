from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import stock_movement as stock_crud
from app.database.database import get_db
from app.schemas.stock_movement import (
    StockAdjustmentCreate,
    StockMovementResponse,
)
from app.schemas.product import ProductResponse


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post(
    "/adjust",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED
)
def adjust_stock(
    adjustment: StockAdjustmentCreate,
    db: Session = Depends(get_db)
):
    movement, error = stock_crud.create_stock_adjustment(
        db,
        adjustment
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return movement


@router.get(
    "/movements",
    response_model=list[StockMovementResponse]
)
def get_stock_movements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return stock_crud.get_stock_movements(
        db,
        skip,
        limit
    )


@router.get(
    "/movements/product/{product_id}",
    response_model=list[StockMovementResponse]
)
def get_product_stock_movements(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return stock_crud.get_product_stock_movements(
        db,
        product_id,
        skip,
        limit
    )


@router.get(
    "/low-stock",
    response_model=list[ProductResponse]
)
def get_low_stock_products(
    db: Session = Depends(get_db)
):
    return stock_crud.get_low_stock_products(db)