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
#  MEDIANAS FIXAS (VALORES PADRÃO SEGUROS)
# ===========================================================

MEDIANA_PRICE: float = 74.99
MEDIANA_FREIGHT: float = 16.28


# ===========================================================
#  FUNÇÃO DE SEGURANÇA PARA PEGAR MEDIANA
# ===========================================================

def get_mediana_segura(valor: Optional[float], fallback: float) -> float:
    """
    Retorna uma mediana válida.
    Se receber None, NaN ou inválido → usa o fallback.
    """
    if valor is None or pd.isna(valor):
        return fallback
    return float(valor)


# ===========================================================
#  AUXILIARES PARA PARSE ROBUSTO
# ===========================================================

def parse_date(valor: Optional[str]) -> Optional[datetime]:
    """Converte string em datetime ou retorna None."""
    if valor is None:
        return None

    valor = str(valor).strip()
    if valor in ("", "nan", "NaN", "None", "null"):
        return None

    dt = pd.to_datetime(valor, errors="coerce")
    if pd.isna(dt):
        return None

    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        dt = dt.tz_localize(None)

    return dt.to_pydatetime()


def parse_numeric(valor: Optional[str]) -> Optional[float]:
    """Converte string numérica em float. Aceita '', 'nan', None."""
    if valor is None:
        return None

    valor = str(valor).strip()

    if valor in ("", "nan", "NaN", "None", "null"):
        return None

    num = pd.to_numeric(valor, errors="coerce")
    return float(num) if pd.notna(num) else None


# ===========================================================
#  🔥 LIMPAR UM ITEM (USA MEDIANAS FIXAS)
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

    # ---------- 2) VALIDAÇÃO DO ORDER_ITEM_ID ----------
    try:
        order_item_id = int(raw.order_item_id)
    except Exception:
        raise ValueError(f"order_item_id inválido: {raw.order_item_id}")

    # ---------- 3) RESGATE DAS MEDIANAS DE FORMA SEGURA ----------
    price_mediana = get_mediana_segura(price_mediana or MEDIANA_PRICE, fallback=0.0)
    freight_mediana = get_mediana_segura(freight_mediana or MEDIANA_FREIGHT, fallback=0.0)

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
        price=float(price),
        freight_value=float(freight_value),
    )


# ===========================================================
#  🔥 FULL LOAD: CALCULA MEDIANAS DE FORMA SEGURA
# ===========================================================

def limpar_itens(
    lista_raw: List[Dict],
    pedidos_ids: Set[str],
    produtos_ids: Set[str],
    vendedores_ids: Set[str],
) -> List[Dict]:

    global MEDIANA_PRICE, MEDIANA_FREIGHT

    df = pd.DataFrame(lista_raw)

    # medianas sempre calculadas com segurança
    price_med = pd.to_numeric(df.get("price"), errors="coerce").median()
    freight_med = pd.to_numeric(df.get("freight_value"), errors="coerce").median()

    # salva medianas somente se forem válidas
    MEDIANA_PRICE = get_mediana_segura(price_med, fallback=MEDIANA_PRICE)
    MEDIANA_FREIGHT = get_mediana_segura(freight_med, fallback=MEDIANA_FREIGHT)

    itens_limpos = []

    for idx, row in enumerate(lista_raw):
        try:
            modelo_raw = ItensPedidosRaw(**row)

            modelo_clean = limpar_um_item(
                modelo_raw,
                pedidos_ids=pedidos_ids,
                produtos_ids=produtos_ids,
                vendedores_ids=vendedores_ids,
                price_mediana=MEDIANA_PRICE,
                freight_mediana=MEDIANA_FREIGHT,
            )

            itens_limpos.append(modelo_clean.model_dump())

        except ValueError as e:
            logger.warning(f"[DESCARTADO] Linha {idx+1}: {e}")

        except Exception as e:
            logger.error(f"[ERRO DESCONHECIDO] Linha {idx+1}: {e}")

    return itens_limpos
