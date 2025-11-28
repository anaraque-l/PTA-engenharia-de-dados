from fastapi import APIRouter
from typing import List
from app.schemas.vendedor_schema import VendedorRaw, VendedorClean
from app.services.vendedor_service import limpar_um_vendedor    

router = APIRouter()


@router.post("/limpar-vendedores", response_model=List[VendedorClean])
def limpar_vendedores(dados: List[VendedorRaw]):

    lista = []

    for vendedor in dados:
        vendedor_limpo = limpar_um_vendedor(vendedor)
        lista.append(vendedor_limpo)

    return lista


@router.post("/tratar-uma-linha")
def tratar_uma_linha(dados: list[VendedorRaw]):

    vendedor = limpar_um_vendedor(dados)

    return {
        "status": "ok",
        "vendedor": vendedor
    }
