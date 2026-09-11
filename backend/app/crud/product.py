from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(
    db: Session,
    product: ProductCreate,
):
    db_product = Product(
        **product.model_dump()
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(Product)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_product(
    db: Session,
    product_id: int,
):
    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )


def get_product_by_sku(
    db: Session,
    sku: str,
):
    return (
        db.query(Product)
        .filter(Product.sku == sku)
        .first()
    )


def update_product(
    db: Session,
    product_id: int,
    product: ProductUpdate,
):
    db_product = get_product(db, product_id)

    if db_product is None:
        return None

    update_data = product.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(
    db: Session,
    product_id: int,
):
    db_product = get_product(db, product_id)

    if db_product is None:
        return None

    db_product.is_active = False

    db.commit()
    db.refresh(db_product)

    return db_product