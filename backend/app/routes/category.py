from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import category as category_crud
from app.database.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    existing_category = category_crud.get_category_by_name(
        db,
        category.name
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists"
        )

    return category_crud.create_category(
        db,
        category
    )


@router.get(
    "/",
    response_model=list[CategoryResponse]
)
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return category_crud.get_categories(
        db,
        skip,
        limit
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = category_crud.get_category(
        db,
        category_id
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
):
    existing_category = category_crud.get_category(
        db,
        category_id
    )

    if existing_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    if category.name is not None:
        duplicate = category_crud.get_category_by_name(
            db,
            category.name
        )

        if duplicate and duplicate.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A category with this name already exists"
            )

    return category_crud.update_category(
        db,
        category_id,
        category
    )


@router.delete(
    "/{category_id}",
    response_model=CategoryResponse
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = category_crud.delete_category(
        db,
        category_id
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category