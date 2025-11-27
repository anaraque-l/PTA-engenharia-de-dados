from typing import List, Set

import pandas as pd
from app.schemas.itenspedidos_schema import ItensPedidosRaw, ItensPedidosClean


def limpar_um_item(raw: ItensPedidosRaw) -> ItensPedidosClean:
    order_id = (raw.order_id or "").strip()
    order_item_id = int(str(raw.order_item_id))
    product_id = (raw.product_id or "").strip()
    seller_id = (raw.seller_id or "").strip()

    price = float(str(raw.price))
    freight_value = float(str(raw.freight_value))

    shipping_limit_date = pd.to_datetime(raw.shipping_limit_date).to_pydatetime()

    return ItensPedidosClean(
        order_id=order_id,
        order_item_id=order_item_id,
        product_id=product_id,
        seller_id=seller_id,
        shipping_limit_date=shipping_limit_date,
        price=price,
        freight_value=freight_value,
    )


def limpar_itens_pedidos(
    raw_data: List[ItensPedidosRaw],
    pedidos_ids: Set[str],
    produtos_ids: Set[str],
    vendedores_ids: Set[str],
) -> List[ItensPedidosClean]:
    itens_limpos: List[ItensPedidosClean] = []

    for raw in raw_data:
        order_id = (raw.order_id or "").strip()
        product_id = (raw.product_id or "").strip()
        seller_id = (raw.seller_id or "").strip()

        if (
            order_id not in pedidos_ids
            or product_id not in produtos_ids
            or seller_id not in vendedores_ids
        ):
            continue

        itens_limpos.append(limpar_um_item(raw))

    return itens_limpos
