from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)


class PurchaseCreate(BaseModel):
    supplier_id: int
    invoice_number: str | None = Field(
        default=None,
        max_length=100
    )
    purchase_date: datetime | None = None
    notes: str | None = Field(
        default=None,
        max_length=255
    )
    items: list[PurchaseItemCreate] = Field(min_length=1)


class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: float
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class PurchaseResponse(BaseModel):
    id: int
    supplier_id: int
    invoice_number: str | None
    purchase_date: datetime
    total_amount: float
    status: str
    notes: str | None
    created_at: datetime
    items: list[PurchaseItemResponse]

    model_config = ConfigDict(from_attributes=True)