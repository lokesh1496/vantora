from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StockAdjustmentCreate(BaseModel):
    product_id: int
    quantity: float
    notes: str | None = Field(
        default=None,
        max_length=255
    )


class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    movement_type: str
    quantity: float
    reference_type: str | None
    reference_id: int | None
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)