from fastapi import APIRouter
from typing import List
import pandas as pd
import logging

from app.schemas.itenspedidos_schema import ItensPedidosRaw, ItensPedidosClean
from app.services.itenspedidos_service import limpar_um_item, MEDIANA_PRICE, MEDIANA_FREIGHT
from app.dados import pedidos_ids, produtos_ids, vendedores_ids

print("Pedidos IDs:", len(pedidos_ids))
print("Produtos IDs:", len(produtos_ids))
print("Vendedores IDs:", len(vendedores_ids))

logger = logging.getLogger(__name__)
router = APIRouter()


# ===========================================================
# 💥 ENDPOINT FULL (processa vários itens)
# ===========================================================
@router.post("/limpar-itens-pedidos", response_model=List[ItensPedidosClean])
def limpar_itens_full(dados: List[ItensPedidosRaw]) -> List[ItensPedidosClean]:
    
    itens_limpos: List[ItensPedidosClean] = []

    for i, item_raw in enumerate(dados):
        try:
            item_clean = limpar_um_item(
                item_raw,
                pedidos_ids,
                produtos_ids,
                vendedores_ids,
                price_mediana=MEDIANA_PRICE,
                freight_mediana=MEDIANA_FREIGHT
            )
            itens_limpos.append(item_clean)

        except ValueError as e:
            logger.warning(f"[DESCARTADO] Item {i+1}: {e}")

        except Exception as e:
            logger.error(f"[ERRO DESCONHECIDO] Item {i+1}: {e}")

    return itens_limpos



# ===========================================================
# ⚡ ENDPOINT INCREMENTAL (somente 1 item)
# ===========================================================
@router.post("/limpar-itens-pedidos-incremental", response_model=List[ItensPedidosClean])
def limpar_itens_incremental(dados: List[ItensPedidosRaw]) -> List[ItensPedidosClean]:

    try:
        # 1) Converte o item em dict exatamente como no FULL LOAD
        raw_dict = dados[0].model_dump()

        # 2) Normaliza via pandas (assim como no FULL LOAD!)
        df = pd.DataFrame([raw_dict])
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["freight_value"] = pd.to_numeric(df["freight_value"], errors="coerce")

        # 3) Converte de volta para dict limpo
        row_clean = df.to_dict(orient="records")[0]

        # 4) Reconstrói o modelo Pydantic (igual ao FULL LOAD)
        modelo_raw = ItensPedidosRaw(**row_clean)

        # 5) Usa as MESMAS medianas globais
        price_mediana = MEDIANA_PRICE if MEDIANA_PRICE is not None else 0.0
        freight_mediana = MEDIANA_FREIGHT if MEDIANA_FREIGHT is not None else 0.0

        # 6) Limpa o item exatamente igual ao FULL LOAD
        item_clean = limpar_um_item(
            modelo_raw,
            pedidos_ids,
            produtos_ids,
            vendedores_ids,
            price_mediana=price_mediana,
            freight_mediana=freight_mediana
        )

        return [item_clean]

    except ValueError as e:
        logger.warning(f"[DESCARTADO] Item incremental falhou. Motivo: {e}")
        return []

    except Exception as e:
        logger.error(f"[ERRO INESPERADO] Item incremental falhou: {e}")
        return []
