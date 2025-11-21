import pandas as pd
from app.schemas.pedidos_schema import PedidosRaw, PedidosClean

def tratar_pedido(dados: PedidosRaw) -> PedidosClean:

    #Limpeza inicial
    order_id = (dados.order_id or "").strip()
    customer_id = (dados.customer_id or "").strip()
    order_status = ((dados.order_status or "").strip()).lower() #A informação "shipped" tinha casos que apareceia como "Shipped"

#--------------------------------------------------------------------------------------------------------------------------------------

    #Corrigindo as datas
    if type(dados.order_purchase_timestamp) == str:
        valor = (dados.order_purchase_timestamp).strip()
    else:
        valor = dados.order_purchase_timestamp

    dt = pd.to_datetime(valor, format="%Y-%m-%d %H:%M:%S", errors="coerce")

    if pd.isna(dt):  
        order_purchase_timestamp = pd.to_datetime("1970-01-01 00:00:00")
    else:
        order_purchase_timestamp = dt

#-----------------

    if type(dados.order_approved_at) == str:
        valor = (dados.order_approved_at).strip()
    else:
        valor = dados.order_approved_at

    dt = pd.to_datetime(valor, format="%Y-%m-%d %H:%M:%S", errors="coerce")

    if pd.isna(dt):  
        order_approved_at = pd.to_datetime("1970-01-01 00:00:00")
    else:
        order_approved_at = dt

#-----------------

    if type(dados.order_delivered_carrier_date) == str:
        valor = (dados.order_delivered_carrier_date).strip()
    else:
        valor = dados.order_delivered_carrier_date

    dt = pd.to_datetime(valor, format="%Y-%m-%d %H:%M:%S", errors="coerce")

    if pd.isna(dt):  
        order_delivered_carrier_date = pd.to_datetime("1970-01-01 00:00:00")
    else:
        order_delivered_carrier_date = dt

#-----------------

    if type(dados.order_delivered_customer_date) == str:
        valor = (dados.order_delivered_customer_date).strip()
    else:
        valor = dados.order_delivered_customer_date

    dt = pd.to_datetime(valor, format="%Y-%m-%d %H:%M:%S", errors="coerce")

    if pd.isna(dt):  
        order_delivered_customer_date = pd.to_datetime("1970-01-01 00:00:00")
    else:
        order_delivered_customer_date = dt

#-----------------

    if type(dados.order_approved_at) == str:
        valor = (dados.order_approved_at).strip()
    else:
        valor = dados.order_approved_at

    dt = pd.to_datetime(valor, format="%Y-%m-%d %H:%M:%S", errors="coerce")

    if pd.isna(dt):  
        order_approved_at = pd.to_datetime("1970-01-01 00:00:00")
    else:
        order_approved_at = dt

#-----------------

    if type(dados.order_estimated_delivery_date) == str:
        valor = (dados.order_estimated_delivery_date).strip()
    else:
        valor = dados.order_estimated_delivery_date

    dt = pd.to_datetime(valor, format="%Y-%m-%d %H:%M:%S", errors="coerce")

    if pd.isna(dt):  
        order_estimated_delivery_date = pd.to_datetime("1970-01-01 00:00:00").date()
    else:
        order_estimated_delivery_date = dt.date()

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