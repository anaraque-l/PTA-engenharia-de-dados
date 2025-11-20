from fastapi import APIRouter
from typing import List
from app.schemas.pedidos_schema import PedidosClean, PedidosRaw
from app.services.pedidos_service import tratar_pedido

router = APIRouter()

@router.post("/limpar-pedidos", response_model=List[PedidosClean])
async def tratar_pedidos(dados: List[PedidosRaw]) -> List[PedidosClean]:
    return [tratar_pedido(pedido) for pedido in dados]