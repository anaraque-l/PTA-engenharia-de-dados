from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.produto_schema import ProdutoRaw, ProdutoClean
from app.services.produto_service import tratar_produtos, tratar_produto_incremental

router = APIRouter()

# -------------------------------------------------------
# FULL LOAD - recebe lista de produtos e devolve lista tratada
# -------------------------------------------------------
@router.post("/limpar-produtos", response_model=List[ProdutoClean])
async def limpar_produtos_endpoint(dados: List[ProdutoRaw]):
    try:
        df = tratar_produtos(dados)
        return df.to_dict(orient="records")     # ← converte DataFrame para lista de dicts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------------------------------
# INCREMENTAL - trata uma ou mais linhas isoladamente
# -------------------------------------------------------
@router.post("/tratar-uma-linha", response_model=List[ProdutoClean])
async def tratar_uma_linha(dados: List[ProdutoRaw]):
    if not dados:
        raise HTTPException(status_code=400, detail="Nenhum dado enviado")

 
     # trata cada linha individualmente
    tratados = [
        tratar_produto_incremental(item.dict())
        for item in dados
    ]
    return tratados
