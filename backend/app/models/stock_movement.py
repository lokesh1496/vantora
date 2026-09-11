from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    movement_type = Column(
        String(30),
        nullable=False,
        index=True
    )

    quantity = Column(
        Float,
        nullable=False
    )

    reference_type = Column(
        String(30),
        nullable=True
    )

    reference_id = Column(
        Integer,
        nullable=True
    )

    notes = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    product = relationship(
        "Product",
        back_populates="stock_movements"
    )