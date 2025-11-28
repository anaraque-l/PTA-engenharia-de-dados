from fastapi import FastAPI
from fastapi import APIRouter
from typing import List
from app.schemas.produto_schema import ProdutoRaw, ProdutoClean
from app.services.produto_service import tratar_produtos

router = APIRouter()

@router.post("/limpar-produtos", response_model=List[ProdutoClean])
async def tratar_pedidos(dados: List[ProdutoRaw]) -> List[ProdutoClean]:
    return tratar_produtos(dados)
