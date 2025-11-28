import pandas as pd
from typing import Optional, List
from datetime import datetime
from app.schemas.pedidos_schema import PedidosRaw, PedidosClean




def parse_date(valor: Optional[str]) -> Optional[datetime]:
    """
    Converte datas usando pandas, retornando None em caso de erro.
    Compatível com os formatos da Olist: YYYY-MM-DD e YYYY-MM-DD HH:MM:SS
    """
    if not valor or str(valor).strip() == "":
        return None

    # Força dayfirst=False para evitar Warning desnecessário
    dt = pd.to_datetime(valor, errors="coerce", dayfirst=False)

    if pd.isna(dt):
        return None

    # Remove timezone, caso exista
    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        dt = dt.tz_localize(None)

    return dt.to_pydatetime()



STATUS_MAP = {
    "delivered": "entregue",
    "invoiced": "faturado",
    "shipped": "enviado",
    "processing": "em processamento",
    "unavailable": "indisponível",
    "canceled": "cancelado",
    "created": "criado",
    "approved": "aprovado",
}


def tratar_pedido(dados: PedidosRaw) -> PedidosClean:
    # Limpeza inicial
    order_id = (dados.order_id or "").strip()
    customer_id = (dados.customer_id or "").strip()
    order_status = ((dados.order_status or "").strip()).lower()
    order_status = STATUS_MAP.get(order_status, order_status)

    # Datas
    order_purchase_timestamp = parse_date(dados.order_purchase_timestamp)
    if order_purchase_timestamp is None:
        raise ValueError("order_purchase_timestamp == None")


    order_approved_at = parse_date(dados.order_approved_at)
    order_delivered_carrier_date = parse_date(dados.order_delivered_carrier_date)
    order_delivered_customer_date = parse_date(dados.order_delivered_customer_date)


    order_estimated_delivery_date = parse_date(dados.order_estimated_delivery_date)
    order_estimated_delivery_date = (
        order_estimated_delivery_date.date() if order_estimated_delivery_date else None
    )

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





# ----------------------------------------------------------------------
# 🔥 FUNÇÃO QUE TRATA LISTA DE PEDIDOS — usada no FULL LOAD e no INCREMENTAL
# ----------------------------------------------------------------------


def tratar_pedidos(lista_raw: List[dict]):
    tratados = []


    for raw in lista_raw:
        modelo_raw = PedidosRaw(**raw)    # cria o modelo Pydantic
        modelo_clean = tratar_pedido(modelo_raw)
        tratados.append(modelo_clean.model_dump())


    return tratados
