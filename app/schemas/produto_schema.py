from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel


class ProdutoRaw(BaseModel):

    product_category_name: str | None = None 
    product_name_lenght: str | None = None
    product_description_lenght: str | None = None 
    product_photos_qty: str | None = None 
    product_weight_g: str | None = None
    product_length_cm: str | None = None 
    product_height_cm: str | None = None 
    product_width_cm: str | None = None 
    
class ProdutoClean(BaseModel):

    categoria_limpa: str
    len_nome_limpa: int
    len_descr_limpa: int
    qtd_fotos_limpa: int
    peso_limpo: float
    comprimento_limpo: float
    altura_limpa: int
    largura_limpa: int

