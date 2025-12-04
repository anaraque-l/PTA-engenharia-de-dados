from fastapi import APIRouter
from typing import List
import logging

from app.schemas.itenspedidos_schema import ItensPedidosRaw, ItensPedidosClean
from app.services.itenspedidos_service import limpar_um_item

# Agora importamos os IDs CARREGADOS pelo startup do main.py
from main import pedidos_ids, produtos_ids, vendedores_ids

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
                vendedores_ids
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

    item_raw = dados[0]   # sempre vem só um item

    try:
        item_clean = limpar_um_item(
            item_raw,
            pedidos_ids,
            produtos_ids,
            vendedores_ids
        )

        return [item_clean]

    except ValueError as e:
        logger.warning(f"[DESCARTADO] Item incremental falhou. Motivo: {e}")
        return []

    except Exception as e:
        logger.error(f"[ERRO INESPERADO] Item incremental: {e}")
        return []
