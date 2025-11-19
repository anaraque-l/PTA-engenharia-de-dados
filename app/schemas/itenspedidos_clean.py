from pydantic import BaseModel
from datetime import datetime

class ItensPedidosClean(BaseModel):
    order_id: str
    order_item_id: int
    product_id: str
    seller_id: str
    shipping_limit_date: datetime
    price: float
    freight_value: float
