import pandas as pd


# ===========================================================
#  MEDIANAS FIXAS (VALORES INICIAIS SEGUROS)
# ===========================================================

MEDIANAS_PRODUTOS = {
    "product_name_lenght": 51,
    "product_description_lenght": 591,
    "product_photos_qty": 1,
    "product_weight_g": 700,
    "product_length_cm": 25,
    "product_height_cm": 13,
    "product_width_cm": 20,
}


# ===========================================================
#  FUNÇÃO DE SEGURANÇA PARA PEGAR MEDIANA SEM RISCO DE NaN
# ===========================================================

def get_mediana_segura(col: str):
    """Retorna valor seguro para a mediana, sem permitir NaN ou None."""
    val = MEDIANAS_PRODUTOS.get(col)

    if val is None or pd.isna(val):
        # fallback seguro
        return 0

    return val



# ===========================================================
#  FULL LOAD - CONSTRÓI AS MEDIANAS
# ===========================================================

def tratar_produtos(dados) -> pd.DataFrame:
    # aceita DataFrame, lista de dicts ou lista de modelos Pydantic
    if isinstance(dados, pd.DataFrame):
        df = dados.copy()
    else:
        linhas = []
        for d in dados:
            if hasattr(d, "dict"):
                linhas.append(d.dict())
            else:
                linhas.append(d)
        df = pd.DataFrame(linhas)

    # categoria limpa
    df['product_category_name'] = (
        df['product_category_name']
        .astype(str)
        .str.strip()
        .replace("", "indefinido")
        .fillna("indefinido")
    )

    colunas = [
        'product_name_lenght',
        'product_description_lenght',
        'product_photos_qty',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]

    # converte para numérico
    for col in colunas:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # calcula medianas APENAS se não forem NaN
    for col in colunas:
        med = df[col].median()
        if not pd.isna(med):
            MEDIANAS_PRODUTOS[col] = med  # atualiza somente se mediana válida

    # preenche usando as medianas seguras
    for col in colunas:
        df[col] = df[col].fillna(get_mediana_segura(col)).astype(int)

    df = df.rename(columns={
        'product_category_name': 'categoria_limpa',
        'product_name_lenght': 'len_nome_limpa',
        'product_description_lenght': 'len_descr_limpa',
        'product_photos_qty': 'qtd_fotos_limpa',
        'product_weight_g': 'peso_limpo',
        'product_length_cm': 'comprimento_limpo',
        'product_height_cm': 'altura_limpa',
        'product_width_cm': 'largura_limpa'
    })

    return df



# ===========================================================
#  INCREMENTAL - USA SEMPRE AS MEDIANAS FIXAS SEGURAS
# ===========================================================

def tratar_produto_incremental(dado: dict) -> dict:
    df = pd.DataFrame([dado])

    df['product_category_name'] = (
        df['product_category_name']
        .astype(str)
        .str.strip()
        .replace("", "indefinido")
        .fillna("indefinido")
    )

    colunas = [
        'product_name_lenght',
        'product_description_lenght',
        'product_photos_qty',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]

    for col in colunas:
        df[col] = pd.to_numeric(df[col], errors='coerce')

        med_seguranca = get_mediana_segura(col)
        df[col] = df[col].fillna(med_seguranca).astype(int)

    df = df.rename(columns={
        'product_category_name': 'categoria_limpa',
        'product_name_lenght': 'len_nome_limpa',
        'product_description_lenght': 'len_descr_limpa',
        'product_photos_qty': 'qtd_fotos_limpa',
        'product_weight_g': 'peso_limpo',
        'product_length_cm': 'comprimento_limpo',
        'product_height_cm': 'altura_limpa',
        'product_width_cm': 'largura_limpa'
    })

    return df.to_dict(orient="records")[0]
