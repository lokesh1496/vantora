from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    product_name: str = Field(
        min_length=1,
        max_length=150
    )

    sku: str = Field(
        min_length=1,
        max_length=50
    )

    barcode: str | None = Field(
        default=None,
        max_length=100
    )

    category_id: int | None = None

    brand: str | None = Field(
        default=None,
        max_length=100
    )

    unit: str = Field(
        min_length=1,
        max_length=30
    )

    purchase_price: float = Field(
        ge=0
    )

    selling_price: float = Field(
        ge=0
    )

    current_stock: float = Field(
        default=0,
        ge=0
    )

    minimum_stock: float = Field(
        default=0,
        ge=0
    )

    maximum_stock: float | None = Field(
        default=None,
        ge=0
    )

    supplier_id: int | None = None

    expiry_date: date | None = None

    batch_number: str | None = Field(
        default=None,
        max_length=100
    )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )

    sku: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    barcode: str | None = Field(
        default=None,
        max_length=100
    )

    category_id: int | None = None

    brand: str | None = Field(
        default=None,
        max_length=100
    )

    unit: str | None = Field(
        default=None,
        min_length=1,
        max_length=30
    )

    purchase_price: float | None = Field(
        default=None,
        ge=0
    )

    selling_price: float | None = Field(
        default=None,
        ge=0
    )

    current_stock: float | None = Field(
        default=None,
        ge=0
    )

    minimum_stock: float | None = Field(
        default=None,
        ge=0
    )

    maximum_stock: float | None = Field(
        default=None,
        ge=0
    )

    supplier_id: int | None = None

    expiry_date: date | None = None

    batch_number: str | None = Field(
        default=None,
        max_length=100
    )

    is_active: bool | None = None


class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )