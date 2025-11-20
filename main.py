from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd # Vamos usar para limpar dados!

app = FastAPI()
# O Cardápio (Define o formato do dado que aceitamos)
class Pedido(BaseModel):
    nome_produto: str
    preco: float | None = None # Aceita nulo

# A Rota (Onde o Garçom atende)
@app.post("/limpar-dados")
def limpar_dados(pedido: Pedido):
    # 1. Tratamento de String (Simples)
    nome_limpo = pedido.nome_produto.lower().strip().replace(" ", "_") 
    # 2. Tratamento de Nulo (Lógica de Negócio)
    if pedido.preco is None:
        preco_final = 0.0 # No desafio real, aqui entra a Mediana!
    else:
        preco_final = pedido.preco
    return {
    "status": "sucesso",
    "nome_tratado": nome_limpo,
    "preco_final": preco_final
}