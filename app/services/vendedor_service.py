import re
from app.schemas.vendedor_raw import VendedorRaw
from app.schemas.vendedor_clean import VendedorClean

def limpar_um_vendedor(raw: VendedorRaw) -> VendedorClean:

    seller_id = (raw.seller_id or "").strip()

    if raw.seller_zip_code_prefix is None:
        zip_code = 0
    else:
        try:
            zip_code = int(str(raw.seller_zip_code_prefix).strip())
        except:
            zip_code = 0

    if raw.seller_city:
        seller_city = raw.seller_city.strip().lower()
        seller_city = re.sub(r"\s+", "_", seller_city)
    else:
        seller_city = "indefinido"

    if raw.seller_state:
        seller_state = raw.seller_state.strip().lower()
        seller_state = re.sub(r"\s+", "_", seller_state)
    else:
        seller_state = "indefinido"

    return VendedorClean(
        seller_id=seller_id,
        seller_zip_code_prefix=zip_code,
        seller_city=seller_city,
        seller_state=seller_state
    )
