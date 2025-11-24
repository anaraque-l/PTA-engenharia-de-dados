import pandas as pd
from typing import Optional
from datetime import datetime
from app.schemas.pedidos_schema import PedidosRaw, PedidosClean

def parse_date(valor: Optional[str]) -> Optional[datetime]:
    
    if not valor:
        return None
    
    dt = pd.to_datetime(valor, errors="coerce")
    
    if pd.isna(dt):
        return None
    else:
        return dt.to_pydatetime()
    
    

def tratar_pedido(dados: PedidosRaw) -> PedidosClean:

    #Limpeza inicial
    order_id = (dados.order_id or "").strip()
    customer_id = (dados.customer_id or "").strip()
    order_status = ((dados.order_status or "").strip()).lower() #A informação "shipped" tinha casos que apareceia como "Shipped"

#--------------------------------------------------------------------------------------------------------------------------------------

    #Corrigindo as datas
    order_purchase_timestamp = parse_date(dados.order_purchase_timestamp)

    if order_purchase_timestamp is None: #Lança o erro em caso de campo obrigatório inválido
        raise ValueError("order_purchase_timestamp == None")

#-----------------

    order_approved_at = parse_date(dados.order_approved_at)

#-----------------

    order_delivered_carrier_date = parse_date(dados.order_delivered_carrier_date)

#-----------------

    order_delivered_customer_date = parse_date(dados.order_delivered_customer_date)

#-----------------

    order_estimated_delivery_date = parse_date(dados.order_estimated_delivery_date)

    order_estimated_delivery_date = (order_estimated_delivery_date.date() if order_estimated_delivery_date else None)

#--------------------------------------------------------------------------------------------------------------------------------------

    return PedidosClean(
        order_id=order_id,
        customer_id=customer_id,
        order_status=order_status,
        order_purchase_timestamp=order_purchase_timestamp,
        order_approved_at=order_approved_at,
        order_delivered_carrier_date=order_delivered_carrier_date,
        order_delivered_customer_date=order_delivered_customer_date,
        order_estimated_delivery_date=order_estimated_delivery_date
    )