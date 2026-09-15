from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import StockAdjustmentCreate


def create_stock_adjustment(
    db: Session,
    adjustment: StockAdjustmentCreate
):
    product = (
        db.query(Product)
        .filter(Product.id == adjustment.product_id)
        .first()
    )

    if product is None:
        return None, "Product not found"

    new_stock = product.current_stock + adjustment.quantity

    # Stock cannot become negative
    if new_stock < 0:
        return None, "Insufficient stock"

    # Update product stock
    product.current_stock = new_stock

    # Determine movement type
    if adjustment.quantity > 0:
        movement_type = "adjustment_in"
    else:
        movement_type = "adjustment_out"

    movement = StockMovement(
        product_id=product.id,
        movement_type=movement_type,
        quantity=adjustment.quantity,
        reference_type="manual_adjustment",
        reference_id=None,
        notes=adjustment.notes,
    )

    db.add(movement)
    db.commit()
    db.refresh(movement)

    return movement, None


def get_stock_movements(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(StockMovement)
        .order_by(StockMovement.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_product_stock_movements(
    db: Session,
    product_id: int,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(StockMovement)
        .filter(StockMovement.product_id == product_id)
        .order_by(StockMovement.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_low_stock_products(
    db: Session
):
    return (
        db.query(Product)
        .filter(
            Product.is_active == True,
            Product.current_stock <= Product.minimum_stock
        )
        .all()
    )