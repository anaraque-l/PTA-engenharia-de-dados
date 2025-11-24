from datetime import datetime
import pandas as pd
from typing import Optional # Importação necessária para tipagem de Optional
from app.schemas.itenspedidos_schema import ItensPedidosRaw, ItensPedidosClean

# Funções auxiliares para parsing
# tratamento de dados com pandas para lidar com valores nulos e formatos incorretos. ( replicar lógica semelhante para pedidos)
def parse_date(valor: Optional[str]) -> Optional[datetime]:
    
    if not valor or pd.isna(valor) or valor.strip() == '1970-01-01 00:00:00':
        return None
    
    
    dt = pd.to_datetime(valor, errors="coerce")
    
    
    return dt.to_pydatetime() if pd.notna(dt) else None

def parse_numeric(valor: Optional[str]) -> Optional[float]:
    
    if not valor:
        return None
        
    
    numeric_value = pd.to_numeric(valor, errors='coerce')
    
    if pd.isna(numeric_value):
        return None
        
    return float(numeric_value)

def limpar_um_item(raw: ItensPedidosRaw) -> ItensPedidosClean:

    # order_id (mantém como veio)
    order_id = raw.order_id

    # order_item_id (converte para int)
    #  adicionando tratamento para nulos/inválidos, quebrando se for crítico (para descarte no router)
    try:
        order_item_id = int(raw.order_item_id) if raw.order_item_id else None
        if order_item_id is None:
            # Assumindo que order_item_id é obrigatório para identificação
            raise ValueError("order_item_id ausente")
    except ValueError:
        # para lançar  erro se for não numérico/inválido para ser pego e descartado pelo router
        raise ValueError(f"order_item_id inválido ou ausente: {raw.order_item_id}")


    # product_id, seller_id (mantém como veio)
    product_id = raw.product_id
    seller_id = raw.seller_id

    # price → float
    #  Usando parse_numeric para tratar nulos e sujeira
    price = parse_numeric(raw.price)

    # freight_value → float
    # Usando parse_numeric para tratar nulos e sujeira
    freight_value = parse_numeric(raw.freight_value)

    # shipping_limit_date → datetime
    # correção Usando parse_date para tratar nulos e formatos inválidos
    shipping_limit_date = parse_date(raw.shipping_limit_date)

    return ItensPedidosClean(
        order_id=order_id,
        order_item_id=order_item_id,
        product_id=product_id,
        seller_id=seller_id,
        shipping_limit_date=shipping_limit_date,
        price=price,
        freight_value=freight_value
    )