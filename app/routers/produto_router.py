from fastapi import FastAPI
from fastapi import APIRouter
from typing import List
from app.schemas.produto_schema import ProdutoRaw, ProdutoClean
from app.services.produto_service import tratar_produtos, tratar_produto_incremental

router = APIRouter()

@router.post("/limpar-produtos", response_model=List[ProdutoClean])
async def tratar_pedidos(dados: List[ProdutoRaw]) -> List[ProdutoClean]:
    return tratar_produtos(dados)

@router.post("/tratar-uma-linha", response_model=ProdutoClean)
def tratar_uma_linha(dado: ProdutoRaw):
    try:
        limpo = tratar_produto_incremental(dado.dict())
        return limpo                         # dict com todas as colunas limpas
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))