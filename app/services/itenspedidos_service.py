import logging
import pandas as pd
from datetime import datetime
from typing import Optional, List, Set, Dict

from app.schemas.itenspedidos_schema import (
    ItensPedidosRaw,
    ItensPedidosClean
)

logger = logging.getLogger(__name__)

# ===========================================================
#  VARIÁVEIS GLOBAIS PARA AS MEDIANAS
#  (usadas no FULL LOAD E NO TRATAR-UMA-LINHA)
# ===========================================================

MEDIANA_PRICE: float = 74.99
MEDIANA_FREIGHT: float = 16.28


# ===========================================================
#  AUXILIARES
# ===========================================================

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
    if valor is None:
        return None

    valor = str(valor).strip()
    if valor == "":
        return None

    num = pd.to_numeric(valor, errors="coerce")
    return float(num) if pd.notna(num) else None


# ===========================================================
#  🔥 LIMPAR SOMENTE UM ITEM (USA MEDIANAS GLOBAIS)
# ===========================================================

def limpar_um_item(
    raw: ItensPedidosRaw,
    pedidos_ids: Set[str],
    produtos_ids: Set[str],
    vendedores_ids: Set[str],
    price_mediana: float | None = None,
    freight_mediana: float | None = None,
) -> ItensPedidosClean:

    # ---------- 1) INTEGRIDADE REFERENCIAL ----------
    if raw.order_id not in pedidos_ids:
        raise ValueError(f"ORFAO: order_id inválido: {raw.order_id}")

    if raw.product_id not in produtos_ids:
        raise ValueError(f"ORFAO: product_id inválido: {raw.product_id}")

    if raw.seller_id not in vendedores_ids:
        raise ValueError(f"ORFAO: seller_id inválido: {raw.seller_id}")

    # ---------- 2) VALIDAÇÃO CRÍTICA ----------
    try:
        order_item_id = int(raw.order_item_id)
    except Exception:
        raise ValueError(f"order_item_id inválido: {raw.order_item_id}")

    # ---------- 3) MEDIANAS (USAR FIXAS SEMPRE) ----------
    price_mediana = MEDIANA_PRICE
    freight_mediana = MEDIANA_FREIGHT

    # price
    price = parse_numeric(raw.price)
    if price is None:
        price = price_mediana

    # freight_value
    freight_value = parse_numeric(raw.freight_value)
    if freight_value is None:
        freight_value = freight_mediana

    # ---------- 4) DATA ----------
    shipping_limit_date = parse_date(raw.shipping_limit_date)

    # ---------- 5) RETORNO ----------
    return ItensPedidosClean(
        order_id=raw.order_id,
        order_item_id=order_item_id,
        product_id=raw.product_id,
        seller_id=raw.seller_id,
        shipping_limit_date=shipping_limit_date,
        price=price,
        freight_value=freight_value
    )



# ===========================================================
#  🔥 LIMPAR LISTA (FULL LOAD) — CALCULA E SALVA MEDIANAS
# ===========================================================

def limpar_itens(
    lista_raw: List[Dict],
    pedidos_ids: Set[str],
    produtos_ids: Set[str],
    vendedores_ids: Set[str],
) -> List[Dict]:

    global MEDIANA_PRICE, MEDIANA_FREIGHT

    df = pd.DataFrame(lista_raw)

    # calcula medianas a partir do dataset completo
    MEDIANA_PRICE = pd.to_numeric(df["price"], errors="coerce").median()
    MEDIANA_FREIGHT = pd.to_numeric(df["freight_value"], errors="coerce").median()

    if pd.isna(MEDIANA_PRICE):
        MEDIANA_PRICE = 0.0
    if pd.isna(MEDIANA_FREIGHT):
        MEDIANA_FREIGHT = 0.0

    itens_limpos = []

    for idx, row in enumerate(lista_raw):
        try:
            modelo_raw = ItensPedidosRaw(**row)

            modelo_clean = limpar_um_item(
                modelo_raw,
                pedidos_ids=pedidos_ids,
                produtos_ids=produtos_ids,
                vendedores_ids=vendedores_ids,
                # aqui eu passo explicitamente, mas também já estão salvas nas globais
                price_mediana=MEDIANA_PRICE,
                freight_mediana=MEDIANA_FREIGHT,
            )

            itens_limpos.append(modelo_clean.model_dump())

        except ValueError as e:
            logger.warning(f"[DESCARTADO] Linha {idx+1}: {e}")

        except Exception as e:
            logger.error(f"[ERRO DESCONHECIDO] Linha {idx+1}: {e}")

    return itens_limpos
