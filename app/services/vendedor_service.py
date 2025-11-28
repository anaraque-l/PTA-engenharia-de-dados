import unidecode
from typing import List
from app.schemas.vendedor_schema import VendedorRaw, VendedorClean


# -------------------------------------------------------
# Função auxiliar de normalização de texto
# -------------------------------------------------------
def normalizar_texto(valor):
    """
    Normaliza valores de texto independentemente do tipo:
    - Converte para string
    - Remove acentos
    - Remove espaços no início/fim
    - Converte para UPPERCASE
    - Se valor for vazio ou None → "INDEFINIDO"
    """
    if valor is None:
        return "INDEFINIDO"

    texto = str(valor).strip()

    if texto == "":
        return "INDEFINIDO"

    texto = unidecode.unidecode(texto)  # remove acentos
    return texto.upper()


# -------------------------------------------------------
# Função que trata UM vendedor
# -------------------------------------------------------
def limpar_um_vendedor(raw: VendedorRaw) -> VendedorClean:

    # seller_id → string segura
    seller_id = normalizar_texto(raw.seller_id)

    # seller_zip_code_prefix → inteiro seguro
    try:
        seller_zip_code_prefix = (
            int(float(raw.seller_zip_code_prefix))
            if raw.seller_zip_code_prefix not in [None, ""]
            else 0
        )
    except Exception:
        seller_zip_code_prefix = 0

    # seller_city → normalização completa
    seller_city = normalizar_texto(raw.seller_city)

    # seller_state → normalização completa
    seller_state = normalizar_texto(raw.seller_state)

    return VendedorClean(
        seller_id=seller_id,
        seller_zip_code_prefix=seller_zip_code_prefix,
        seller_city=seller_city,
        seller_state=seller_state
    )


# -------------------------------------------------------
# Função que trata LISTA DE VENDEDORES (FULL LOAD)
# -------------------------------------------------------
def tratar_vendedores(lista_raw: List[dict]):
    vendedores_limpos = []

    for raw in lista_raw:
        try:
            modelo_raw = VendedorRaw(**raw)
            modelo_clean = limpar_um_vendedor(modelo_raw)
            vendedores_limpos.append(modelo_clean.model_dump())
        except Exception as e:
            # Se quiser logar:
            # print(f"[WARN] Registro descartado: {e}")
            continue

    return vendedores_limpos
