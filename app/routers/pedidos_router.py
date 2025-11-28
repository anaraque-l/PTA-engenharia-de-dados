from fastapi import APIRouter
from typing import List
from app.schemas.pedidos_schema import PedidosClean, PedidosRaw
from app.services.pedidos_service import tratar_pedido, tratar_pedidos


router = APIRouter()







# ------------------------------------------------------------------------------
# 1) LOTE COMPLETO — /limpar-pedidos
# ------------------------------------------------------------------------------
@router.post("/limpar-pedidos", response_model=List[PedidosClean])
async def limpar_pedidos(dados: List[PedidosRaw]) -> List[PedidosClean]:
   
    pedidos_validos = []


    for pedido in dados:
        try:
            tratado = tratar_pedido(pedido)
            pedidos_validos.append(tratado)
        except ValueError:
            # descarta esse registro e continua
            continue


    return pedidos_validos




# ------------------------------------------------------------------------------
# 2) TRATAR UMA LINHA — /tratar-uma-linha
# ------------------------------------------------------------------------------
@router.post("/tratar-uma-linha")
async def tratar_uma_linha(dados: list[PedidosRaw]):
   
    try:
        tratado = tratar_pedido(dados)
        return {"status": "ok", "pedido": tratado}


    except ValueError as e:
        return {"status": "descartado", "motivo": str(e)}
