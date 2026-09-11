from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import supplier as supplier_crud
from app.database.database import get_db
from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)


@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db)
):
    existing_supplier = supplier_crud.get_supplier_by_company_name(
        db,
        supplier.company_name
    )

    if existing_supplier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A supplier with this company name already exists"
        )

    return supplier_crud.create_supplier(db, supplier)


@router.get(
    "/",
    response_model=list[SupplierResponse]
)
def get_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return supplier_crud.get_suppliers(
        db,
        skip,
        limit
    )


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    supplier = supplier_crud.get_supplier(
        db,
        supplier_id
    )

    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    return supplier


@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db)
):
    existing_supplier = supplier_crud.get_supplier(
        db,
        supplier_id
    )

    if existing_supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    if supplier.company_name is not None:
        duplicate = supplier_crud.get_supplier_by_company_name(
            db,
            supplier.company_name
        )

        if duplicate and duplicate.id != supplier_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A supplier with this company name already exists"
            )

    return supplier_crud.update_supplier(
        db,
        supplier_id,
        supplier
    )


@router.delete(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    supplier = supplier_crud.delete_supplier(
        db,
        supplier_id
    )

    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    return supplier