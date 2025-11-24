import pandas as pd 
from app.schemas.produto_schema import ProdutoRaw, ProdutoClean

def tratar_produtos(dados: ProdutoRaw) -> ProdutoClean:

    dados = [produto.model_dump() for produto in dados]
    df = pd.DataFrame(dados)

    # limpando a coluna do nome da categoria
    df['product_category_name'] = df['product_category_name'].str.lower().str.strip()
    df['product_category_name'] = df['product_category_name'].str.replace(" ", "_")
    df['product_category_name'] = df['product_category_name'].fillna("indefinido")

    # garantindo que todas as colunas numéricas estão efetivamente em formatos numéricos
    df['product_name_lenght'] = pd.to_numeric(df['product_name_lenght'], errors='coerce')
    df['product_description_lenght'] = pd.to_numeric(df['product_description_lenght'], errors='coerce')
    df['product_weight_g'] = pd.to_numeric(df['product_weight_g'], errors='coerce')
    df['product_photos_qty'] = pd.to_numeric(df['product_photos_qty'], errors='coerce')
    df['product_length_cm'] = pd.to_numeric(df['product_length_cm'], errors='coerce')
    df['product_height_cm'] = pd.to_numeric(df['product_height_cm'], errors='coerce')
    df['product_width_cm'] = pd.to_numeric(df['product_width_cm'], errors='coerce')

    # calculando as médias de cada coluna numérica
    mediana_len_nome = df['product_name_lenght'].median()
    mediana_len_descr = df['product_description_lenght'].median()
    mediana_qtd_fotos = df['product_photos_qty'].median()
    mediana_peso = df['product_weight_g'].median()
    mediana_comprimento = df['product_length_cm'].median()
    mediana_altura = df['product_height_cm'].median()
    mediana_largura =  df['product_width_cm'].median()

    # preenchendo os valores vazios das colunas numéricas com as médias
    df['product_name_lenght'] = df['product_name_lenght'].fillna(mediana_len_nome)
    df['product_description_lenght'] = df['product_description_lenght'].fillna(mediana_len_descr)
    df['product_photos_qty'] = df['product_photos_qty'].fillna(mediana_qtd_fotos)
    df['product_weight_g'] = df['product_weight_g'].fillna(mediana_peso)
    df['product_length_cm'] = df['product_length_cm'].fillna(mediana_comprimento)
    df['product_height_cm'] = df['product_height_cm'].fillna(mediana_altura)
    df['product_width_cm'] = df['product_width_cm'].fillna(mediana_largura)

    # convertendo para inteiro as colunas que devem sê-los (pois a função to_numeric torna tudo float quando encontra algum NaN)

    df['product_name_lenght'] = df['product_name_lenght'].astype(int)
    df['product_description_lenght'] = df['product_description_lenght'].astype(int)
    df['product_photos_qty'] = df['product_photos_qty'].astype(int)
    df['product_length_cm'] = df['product_length_cm'].astype(int)
    df['product_height_cm'] = df['product_height_cm'].astype(int)
    df['product_width_cm'] = df['product_width_cm'].astype(int)

    # renomeando os dados, para entendermos quais são os sujos e quais são os limpos
    mapa_renomeacao = {'product_category_name': 'categoria_limpa', 
                   'product_name_lenght': 'len_nome_limpa', 
                   'product_description_lenght': 'len_descr_limpa',
                   'product_photos_qty': 'qtd_fotos_limpa',
                   'product_weight_g': 'peso_limpo',
                   'product_length_cm': 'comprimento_limpo',
                   'product_height_cm': 'altura_limpa',
                   'product_width_cm': 'largura_limpa'}
    
    df = df.rename(columns=mapa_renomeacao)

    return df.to_dict(orient="records") # para retornar em um formato que a API entende


