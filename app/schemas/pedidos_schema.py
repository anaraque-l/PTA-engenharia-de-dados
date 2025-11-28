from pydantic import BaseModel
from datetime import datetime, date

class PedidosRaw(BaseModel):
    order_id: str | None = None
    customer_id: str | None = None
    order_status: str | None = None
    order_purchase_timestamp: str | None = None
    order_approved_at: str | None = None
    order_delivered_carrier_date: str | None = None
    order_delivered_customer_date: str | None = None
    order_estimated_delivery_date: str | None = None

class PedidosClean(BaseModel):
    order_id: str
    customer_id: str
    order_status: str
    order_purchase_timestamp: datetime
    order_approved_at: datetime | None
    order_delivered_carrier_date: datetime | None
    order_delivered_customer_date: datetime | None
    order_estimated_delivery_date: date
    tempo_entrega_dias: int | None
    tempo_entrega_estimado_dias: int | None
    diferenca_entrega_dias: int | None
    entrega_no_prazo: str