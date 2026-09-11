from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_name = Column(
        String(150),
        nullable=False,
        index=True
    )

    sku = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    barcode = Column(
        String(100),
        unique=True,
        nullable=True,
        index=True
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True
    )

    brand = Column(
        String(100),
        nullable=True
    )

    unit = Column(
        String(30),
        nullable=False
    )

    purchase_price = Column(
        Float,
        nullable=False
    )

    selling_price = Column(
        Float,
        nullable=False
    )

    current_stock = Column(
        Float,
        nullable=False,
        default=0
    )

    minimum_stock = Column(
        Float,
        nullable=False,
        default=0
    )

    maximum_stock = Column(
        Float,
        nullable=True
    )

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=True
    )

    expiry_date = Column(
        Date,
        nullable=True
    )

    batch_number = Column(
        String(100),
        nullable=True
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        nullable=True,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    supplier = relationship(
        "Supplier",
        back_populates="products"
    )
    stock_movements = relationship(
    "StockMovement",
    back_populates="product"
)