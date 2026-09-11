from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def create_supplier(db: Session, supplier: SupplierCreate):
    db_supplier = Supplier(**supplier.model_dump())

    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    return db_supplier


def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Supplier)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )


def get_supplier_by_company_name(
    db: Session,
    company_name: str
):
    return (
        db.query(Supplier)
        .filter(Supplier.company_name == company_name)
        .first()
    )


def update_supplier(
    db: Session,
    supplier_id: int,
    supplier: SupplierUpdate
):
    db_supplier = get_supplier(db, supplier_id)

    if db_supplier is None:
        return None

    update_data = supplier.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_supplier, field, value)

    db.commit()
    db.refresh(db_supplier)

    return db_supplier


def delete_supplier(db: Session, supplier_id: int):
    db_supplier = get_supplier(db, supplier_id)

    if db_supplier is None:
        return None

    # Soft delete
    db_supplier.is_active = False

    db.commit()
    db.refresh(db_supplier)

    return db_supplier