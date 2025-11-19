from pydantic import BaseModel

class ItensPedidosRaw(BaseModel):
    order_id: str | None = None
    order_item_id: str | None = None
    product_id: str | None = None
    seller_id: str | None = None
    shipping_limit_date: str | None = None
    price: str | None = None
    freight_value: str | None = None
