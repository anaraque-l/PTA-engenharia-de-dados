import pandas as pd 
from app.schemas.produto_schema import ProdutoRaw, ProdutoClean

def tratar_produtos(dados: list[ProdutoRaw]) -> ProdutoClean:

    # Converte lista de Pydantic para lista de dicts
    dados = [produto.model_dump() for produto in dados]
    df = pd.DataFrame(dados)

    # Padroniza nulos de texto
    df = df.replace({None: "", "null": "", "None": ""})

    # 1) Categoria: lowercase + strip + replace + indefinido
    df["product_category_name"] = (
        df["product_category_name"]
        .astype(str)
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .replace("", "indefinido")
    )

    # 2) Convertendo números
    colunas_num = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    df[colunas_num] = df[colunas_num].apply(pd.to_numeric, errors="coerce")

    # 3) Preenchendo com mediana
    for col in colunas_num:
        mediana = df[col].median()
        if pd.isna(mediana):  # caso todos sejam NaN
            mediana = 0
        df[col] = df[col].fillna(mediana).astype(int)

    # 4) Renomeando
    df = df.rename(
        columns={
            "product_category_name": "categoria_limpa",
            "product_name_lenght": "len_nome_limpa",
            "product_description_lenght": "len_descr_limpa",
            "product_photos_qty": "qtd_fotos_limpa",
            "product_weight_g": "peso_limpo",
            "product_length_cm": "comprimento_limpo",
            "product_height_cm": "altura_limpa",
            "product_width_cm": "largura_limpa",
        }
    )

    return df.to_dict(orient="records")


