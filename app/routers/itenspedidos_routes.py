from fastapi import APIRouter
from typing import List, Optional
import logging

from app.schemas.itenspedidos_schema import ItensPedidosRaw
from app.schemas.itenspedidos_schema import ItensPedidosClean
from app.services.itenspedidos_service import limpar_um_item

# Configura o logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/limpar-itens-pedidos", response_model=List[ItensPedidosClean])
def limpar_itens(dados: List[ItensPedidosRaw]) -> List[ItensPedidosClean]:
    
    # Lista para armazenar apenas os registros limpos e válidos
    itens_limpos: List[ItensPedidosClean] = []
    
    # Processa cada item individualmente para aplicar o descarte seletivo
    for i, item_raw in enumerate(dados):
        try:
            # tenta limpar o item (aqui o service lança ValueError se order_item_id for inválido)
            item_clean = limpar_um_item(item_raw)
            itens_limpos.append(item_clean)
            
        except ValueError as e:
            # Captura a exceção lançada pelo service e descarta o registro.
            # para ajudar vocês em debugs futuros, adicionei o motivo de descarte no log 
            logger.warning(f"DESCARTE DE REGISTRO: Item {i+1} falhou na validação de dados críticos. Motivo: {e}")
            
        except Exception as e:
            # captura qualquer outra exceção inesperada 
            logger.error(f"ERRO INESPERADO: Item {i+1} falhou com erro desconhecido: {e}")

    # Retorna a lista de itens limpos. 
    return itens_limpos