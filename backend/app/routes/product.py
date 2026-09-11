from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import product as product_crud
from app.database.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    existing_product = product_crud.get_product_by_sku(
        db,
        product.sku
    )

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A product with this SKU already exists"
        )

    return product_crud.create_product(
        db,
        product
    )


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return product_crud.get_products(
        db,
        skip,
        limit
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = product_crud.get_product(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    existing_product = product_crud.get_product(
        db,
        product_id
    )

    if existing_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.sku is not None:
        sku_product = product_crud.get_product_by_sku(
            db,
            product.sku
        )

        if sku_product and sku_product.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A product with this SKU already exists"
            )

    return product_crud.update_product(
        db,
        product_id,
        product
    )


@router.delete(
    "/{product_id}",
    response_model=ProductResponse
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = product_crud.delete_product(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product