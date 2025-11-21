from datetime import datetime
import pandas as pd
from app.schemas.itenspedidos_schema import ItensPedidosRaw, ItensPedidosClean

def limpar_um_item(raw: ItensPedidosRaw) -> ItensPedidosClean:

    # order_id (mantém como veio)
    order_id = raw.order_id

    # order_item_id (converte para int)
    order_item_id = int(raw.order_item_id)

    # product_id, seller_id (mantém como veio)
    product_id = raw.product_id
    seller_id = raw.seller_id

    # price → float
    price = float(raw.price)

    # freight_value → float
    freight_value = float(raw.freight_value)

    # shipping_limit_date → datetime
    shipping_limit_date = pd.to_datetime(raw.shipping_limit_date).to_pydatetime()

    return ItensPedidosClean(
        order_id=order_id,
        order_item_id=order_item_id,
        product_id=product_id,
        seller_id=seller_id,
        shipping_limit_date=shipping_limit_date,
        price=price,
        freight_value=freight_value
    )
