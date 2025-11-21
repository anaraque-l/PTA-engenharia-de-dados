from fastapi import APIRouter
from typing import List

from app.schemas.itenspedidos_schema import ItensPedidosRaw
from app.schemas.itenspedidos_schema import ItensPedidosClean
from app.services.itenspedidos_service import limpar_um_item

router = APIRouter()

@router.post("/limpar-itens-pedidos", response_model=List[ItensPedidosClean])
async def limpar_itens(dados: List[ItensPedidosRaw]) -> List[ItensPedidosClean]:
    return [limpar_um_item(item) for item in dados]
