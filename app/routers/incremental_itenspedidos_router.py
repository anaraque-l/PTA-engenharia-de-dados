from fastapi import APIRouter
import logging
from typing import List

from app.schemas.itenspedidos_schema import ItensPedidosRaw
from app.schemas.itenspedidos_schema import ItensPedidosClean
from app.services.itenspedidos_service import limpar_um_item

# Configura o logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/limpar-itens-pedidos-incremental", response_model=List[ItensPedidosClean])
def limpar_itens(dados: List[ItensPedidosRaw]) -> List[ItensPedidosClean]:
    
    # Processa o item para aplicar o descarte seletivo
    try:
        # tenta limpar o item (aqui o service lança ValueError se order_item_id for inválido)
        item_clean = limpar_um_item(dados[0])
            
    except ValueError as e:
        # Captura a exceção lançada pelo service e descarta o registro.
        # para ajudar vocês em debugs futuros, adicionei o motivo de descarte no log 
        logger.warning(f"DESCARTE DE REGISTRO: Item 1 (único) falhou na validação de dados críticos. Motivo: {e}")
            
    except Exception as e:
        # captura qualquer outra exceção inesperada 
        logger.error(f"ERRO INESPERADO: Item 1 (único) falhou com erro desconhecido: {e}")

    # Retorna uma lista de um item limpo 
    return [item_clean]