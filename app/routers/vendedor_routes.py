from fastapi import APIRouter
from typing import List
from app.schemas.vendedor_raw import VendedorRaw
from app.schemas.vendedor_clean import VendedorClean
from app.services.vendedor_service import limpar_um_vendedor

router = APIRouter()

@router.post("/limpar-vendedores", response_model=List[VendedorClean])
async def limpar_vendedores(dados: List[VendedorRaw]) -> List[VendedorClean]:
    return [limpar_um_vendedor(v) for v in dados]
