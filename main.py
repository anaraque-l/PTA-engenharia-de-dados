from fastapi import FastAPI
import uvicorn

from app.routers.produto_router import router as produto_router

app = FastAPI(
    title="API de Tratamento de Dados - Desafio 1",
    description="API que recebe dados brutos, os trata e os devolve limpos.",
    version="1.0.0"
)

# REGISTRO DOS ROUTERS
app.include_router(produto_router, prefix="/produto", tags=["Produtos"])

# ROTAS FIXAS
@app.get("/", description="Mensagem de boas-vindas da API.")
async def read_root():
    return {"message": "Bem-vindo à API de Tratamento de Dados!"}

@app.get("/health", description="Verifica a saúde da API.")
async def health_check():
    return {"status": "ok"}