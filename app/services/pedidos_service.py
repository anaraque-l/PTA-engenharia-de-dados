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

    status_map = {
    "delivered": "entregue",
    "invoiced": "faturado",
    "shipped": "enviado",
    "processing": "em processamento",
    "unavailable": "indisponível",
    "canceled": "cancelado",
    "created": "criado",
    "approved": "aprovado"
    }

    order_status = ((dados.order_status or "").strip()).lower() #A informação "shipped" tinha casos que apareceia como "Shipped"
    order_status = status_map.get(order_status, order_status)

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
# Novos campos

    # Tempo de entrega em dias
    if order_delivered_customer_date:
        tempo_entrega_dias = (order_delivered_customer_date - order_purchase_timestamp).days
    else:
        tempo_entrega_dias = None

    # Tempo de entrega estimado em dias
    if order_estimated_delivery_date:
        tempo_entrega_estimado_dias = (order_estimated_delivery_date - order_purchase_timestamp.date()).days
    else:
        tempo_entrega_estimado_dias = None

    # Diferenca entrega em dias
    if tempo_entrega_dias is not None and tempo_entrega_estimado_dias is not None:
        diferenca_entrega_dias = tempo_entrega_dias - tempo_entrega_estimado_dias
    else:
        diferenca_entrega_dias = None

    # Entrega no prazo
    if tempo_entrega_dias is None:
        entrega_no_prazo = "Não Entregue"
    else:
        entrega_no_prazo = "Sim" if diferenca_entrega_dias <= 0 else "Não"

    return PedidosClean(
        order_id=order_id,
        customer_id=customer_id,
        order_status=order_status,
        order_purchase_timestamp=order_purchase_timestamp,
        order_approved_at=order_approved_at,
        order_delivered_carrier_date=order_delivered_carrier_date,
        order_delivered_customer_date=order_delivered_customer_date,
        order_estimated_delivery_date=order_estimated_delivery_date,
        
        tempo_entrega_dias=tempo_entrega_dias,
        tempo_entrega_estimado_dias=tempo_entrega_estimado_dias,
        diferenca_entrega_dias=diferenca_entrega_dias,
        entrega_no_prazo=entrega_no_prazo
    )