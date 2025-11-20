import pandas as pd


class ProdutoRaw(BaseModel):

    categoria: str | None = None 
    len_nome: int | None = None
    len_descr: int | None = None 
    qtd_fotos: int | None = None 
    peso: float | None = None
    comprimento: float | None = None 
    altura: int | None = None 
    largura: int | None = None 


class ProdutoClean(BaseModel):

    categoria_limpa: str
    len_nome_limpa: int
    len_descr_limpa: int
    qtd_fotos_limpa: int
    peso_limpa: float
    comprimento_limpa: float
    altura_limpa: int
    largura_limpa: int

def tratar_produtos(produtos_raw:list[ProdutoRaw]):

    dados = [produto.model_dump() for produto in produtos_raw]
    df = pd.DataFrame(dados)

    df['product_category_name'] = df['product_category_name'].str.lower().str.strip()




