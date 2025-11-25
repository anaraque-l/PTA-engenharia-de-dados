from typing import List, Set

from fastapi import APIRouter, Depends

from app.schemas.itenspedidos_schema import ItensPedidosRaw, ItensPedidosClean
from app.services.itenspedidos_service import limpar_itens_pedidos

router = APIRouter()


async def get_pedidos_ids() -> Set[str]:
    return {"order_0001", "order_0002", "order_0003"}


async def get_produtos_ids() -> Set[str]:
    return {"prod_0001", "prod_0002", "prod_0003"}


async def get_vendedores_ids() -> Set[str]:
    return {"seller_0001", "seller_0002", "seller_0003"}


@router.post(
    "/limpar-itens-pedidos",
    response_model=List[ItensPedidosClean],
)
async def limpar_e_validar_itens_pedidos(
    itens_raw: List[ItensPedidosRaw],
    pedidos_ids: Set[str] = Depends(get_pedidos_ids),
    produtos_ids: Set[str] = Depends(get_produtos_ids),
    vendedores_ids: Set[str] = Depends(get_vendedores_ids),
):
    return limpar_itens_pedidos(
        raw_data=itens_raw,
        pedidos_ids=pedidos_ids,
        produtos_ids=produtos_ids,
        vendedores_ids=vendedores_ids,
    )
