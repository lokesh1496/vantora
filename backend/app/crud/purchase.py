from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.purchase import Purchase, PurchaseItem
from app.models.stock_movement import StockMovement
from app.models.supplier import Supplier
from app.schemas.purchase import PurchaseCreate


def create_purchase(db: Session, purchase_data: PurchaseCreate):
    # Check supplier
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == purchase_data.supplier_id)
        .first()
    )

    if supplier is None:
        return None, "Supplier not found"

    purchase = Purchase(
        supplier_id=purchase_data.supplier_id,
        invoice_number=purchase_data.invoice_number,
        purchase_date=purchase_data.purchase_date,
        notes=purchase_data.notes,
        total_amount=0,
        status="completed",
    )

    db.add(purchase)
    db.flush()

    total_amount = 0

    for item_data in purchase_data.items:

        # Find product
        product = (
            db.query(Product)
            .filter(Product.id == item_data.product_id)
            .first()
        )

        if product is None:
            db.rollback()
            return None, f"Product {item_data.product_id} not found"

        # Calculate item total
        item_total = item_data.quantity * item_data.unit_price

        purchase_item = PurchaseItem(
            purchase_id=purchase.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            total_price=item_total,
        )

        db.add(purchase_item)

        # Increase product stock
        product.current_stock += item_data.quantity

        # Record stock movement
        movement = StockMovement(
            product_id=product.id,
            movement_type="purchase",
            quantity=item_data.quantity,
            reference_type="purchase",
            reference_id=purchase.id,
            notes=f"Stock added from purchase #{purchase.id}",
        )

        db.add(movement)

        total_amount += item_total

    purchase.total_amount = total_amount

    db.commit()
    db.refresh(purchase)

    return purchase, None


def get_purchases(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(Purchase)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_purchase(
    db: Session,
    purchase_id: int
):
    return (
        db.query(Purchase)
        .filter(Purchase.id == purchase_id)
        .first()
    )