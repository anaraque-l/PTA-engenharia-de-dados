import pandas as pd
from datetime import datetime
from app.schemas.itenspedidos_schema import ItensPedidosRaw
from app.schemas.itenspedidos_schema import ItensPedidosClean

def limpar_um_item(raw: ItensPedidosRaw) -> ItensPedidosClean:

    # -----------------------------
    # LIMPEZA BÁSICA
    # -----------------------------
    order_id = (raw.order_id or "").strip()
    product_id = (raw.product_id or "").strip()
    seller_id = (raw.seller_id or "").strip()

    # order_item_id → int
    try:
        order_item_id = int(str(raw.order_item_id).strip())
    except:
        order_item_id = 0

    # price → float
    try:
        price = float(str(raw.price).strip())
    except:
        price = 0.0

    # freight_value → float
    try:
        freight_value = float(str(raw.freight_value).strip())
    except:
        freight_value = 0.0

    # -----------------------------
    # CONVERSÃO DA DATA
    # -----------------------------
    if raw.shipping_limit_date:
        dt = pd.to_datetime(raw.shipping_limit_date, errors="coerce")
        if pd.isna(dt):
            shipping_limit_date = pd.Timestamp("1970-01-01")
        else:
            shipping_limit_date = dt.to_pydatetime()
    else:
        shipping_limit_date = pd.Timestamp("1970-01-01").to_pydatetime()

    return ItensPedidosClean(
        order_id=order_id,
        order_item_id=order_item_id,
        product_id=product_id,
        seller_id=seller_id,
        shipping_limit_date=shipping_limit_date,
        price=price,
        freight_value=freight_value
    )
