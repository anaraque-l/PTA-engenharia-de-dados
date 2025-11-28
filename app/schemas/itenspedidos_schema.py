from pydantic import BaseModel
from datetime import datetime

class ItensPedidosRaw(BaseModel):
    order_id: str | None = None
    order_item_id: str| int | None = None
    product_id: str | None = None
    seller_id: str | None = None
    shipping_limit_date: str | None = None
    price: str | float | None = None
    freight_value: str | float | None = None

class ItensPedidosClean(BaseModel):
    order_id: str
    order_item_id: int 
    product_id: str
    seller_id: str
    shipping_limit_date: datetime
    price: float
    freight_value: float 