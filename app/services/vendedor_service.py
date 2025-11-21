import unidecode
from app.schemas.vendedor_schema import VendedorClean
from app.schemas.vendedor_schema import VendedorRaw


def limpar_um_vendedor(raw: VendedorRaw) -> VendedorClean:
    # 1. seller_id
    seller_id = (raw.seller_id or "").strip()

    # 2. seller_zip_code_prefix -> converte para int se possível
    try:
        seller_zip_code_prefix = int(float(raw.seller_zip_code_prefix)) \
            if raw.seller_zip_code_prefix is not None else 0
    except ValueError:
        seller_zip_code_prefix = 0

    # 3. seller_city — REMOVER ACENTO + UPPERCASE
    if raw.seller_city:
        seller_city = unidecode.unidecode(raw.seller_city.strip()).upper()
    else:
        seller_city = "INDEFINIDO"

    # 4. seller_state — REMOVER ACENTO + UPPERCASE
    if raw.seller_state:
        seller_state = unidecode.unidecode(raw.seller_state.strip()).upper()
    else:
        seller_state = "INDEFINIDO"

    # 5. Retorna modelo CLEAN
    return VendedorClean(
        seller_id=seller_id,
        seller_zip_code_prefix=seller_zip_code_prefix,
        seller_city=seller_city,
        seller_state=seller_state
    )
