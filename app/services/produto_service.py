import pandas as pd 
from app.schemas.produto_schema import ProdutoRaw, ProdutoClean

def tratar_produtos(dados: ProdutoRaw) -> ProdutoClean:

    dados = [produto.model_dump() for produto in ProdutoRaw]
    df = pd.DataFrame(dados)

    # limpando a coluna do nome da categoria
    df['product_category_name'] = df['product_category_name'].str.lower().str.strip()
    df['product_category_name'] = df['product_category_name'].str.replace(" ", "_")
    df['product_category_name'] = df['product_category_name'].fillna("indefinido")

    # garantindo que todas as colunas numéricas estão efetivamente em formatos numéricos
    df['product_name_lenght'] = df['product_name_lenght'].astype(int)
    df['product_weight_g'] = df['product_weight_g'].astype(float)
    df['product_photos_qty'] = df['product_photos_qty'].astype(int)
    df['product_length_cm'] = df['product_length_cm'].astype(int)
    df['product_height_cm'] = df['product_height_cm'].astype(int)
    df['product_width_cm'] = df['product_width_cm'].astype(int)

    # calculando as médias de cada coluna numérica
    media_len_nome = df['product_name_lenght'].mean()
    media_qtd_fotos = df['product_photos_qty'].mean()
    media_peso = df['product_weight_g'].mean()
    media_comprimento = df['product_length_cm'].mean()
    media_altura = df['product_height_cm'].mean()

    # preenchendo os valores vazios das colunas numéricas com as médias
    df['product_name_lenght'] = df['product_name_lenght'].fillna(media_len_nome)
    df['product_photos_qty'] = df['product_photos_qty'].fillna(media_qtd_fotos)
    df['product_weight_g'] = df['product_weight_g'].fillna(media_peso)
    df['product_length_cm'] = df['product_length_cm'].fillna()
    df['product_height_cm'] = df['product_height_cm'].fillna(media_comprimento)
    df['product_height_cm'] = df['product_height_cm'].fillna(media_altura)


