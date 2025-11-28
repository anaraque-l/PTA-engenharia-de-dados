import logging
import pandas as pd
from typing import Optional, List
from datetime import datetime
from app.schemas.itenspedidos_schema import ItensPedidosRaw, ItensPedidosClean

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------

def parse_date(valor: Optional[str]) -> Optional[datetime]:
    if not valor or str(valor).strip() == "":
        return None

    dt = pd.to_datetime(valor, errors="coerce")

    if pd.isna(dt):
        return None

    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        dt = dt.tz_localize(None)

    return dt.to_pydatetime()


def parse_numeric(valor: Optional[str]) -> Optional[float]:
    if not valor:
        return None

    num = pd.to_numeric(valor, errors="coerce")

    return float(num) if pd.notna(num) else None


# ---------------------------------------------------------
# Função principal para limpar 1 item
# ---------------------------------------------------------

def limpar_um_item(raw: ItensPedidosRaw) -> ItensPedidosClean:

    # order_id
    order_id = raw.order_id

    # order_item_id -> obrigatório
    try:
        order_item_id = int(raw.order_item_id)
    except Exception:
        raise ValueError(f"order_item_id inválido: {raw.order_item_id}")

    # product_id e seller_id
    product_id = raw.product_id
    seller_id = raw.seller_id

    # price
    price = parse_numeric(str(raw.price))

    # freight_value
    freight_value = parse_numeric(str(raw.freight_value))

    # shipping_limit_date
    shipping_limit_date = parse_date(raw.shipping_limit_date)

    return ItensPedidosClean(
        order_id=order_id,
        order_item_id=order_item_id,
        product_id=product_id,
        seller_id=seller_id,
        shipping_limit_date=shipping_limit_date,
        price=price,
        freight_value=freight_value
    )


# ---------------------------------------------------------
# Função que limpa LISTA — FULL LOAD
# ---------------------------------------------------------

def limpar_itens(lista_raw: List[dict]) -> List[dict]:

    itens_limpos = []

    for i, d in enumerate(lista_raw):

        try:
            # transforme o dict em pydantic
            modelo_raw = ItensPedidosRaw(**d)

            modelo_clean = limpar_um_item(modelo_raw)

            itens_limpos.append(modelo_clean.model_dump())

        except ValueError as e:
            logger.warning(f"[DESCARTADO] Registro {i+1}: {e}")

        except Exception as e:
            logger.error(f"[ERRO] Registro {i+1}: {e}")

    return itens_limpos
