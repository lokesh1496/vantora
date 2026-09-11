from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import purchase as purchase_crud
from app.database.database import get_db
from app.schemas.purchase import (
    PurchaseCreate,
    PurchaseResponse,
)


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


@router.post(
    "/",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db)
):
    result, error = purchase_crud.create_purchase(
        db,
        purchase
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return result


@router.get(
    "/",
    response_model=list[PurchaseResponse]
)
def get_purchases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return purchase_crud.get_purchases(
        db,
        skip,
        limit
    )


@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    purchase = purchase_crud.get_purchase(
        db,
        purchase_id
    )

    if purchase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found"
        )

    return purchase