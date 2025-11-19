from fastapi import FastAPI
from app.routers.vendedor_routes import router as vendedor_router
from app.routers.example import router as example_router

app = FastAPI(
    title="API de Tratamento de Dados - Desafio 1",
    description="API que recebe dados brutos, os trata e os devolve limpos.",
    version="1.0.0"
)

# REGISTRO DOS ROUTERS
app.include_router(vendedor_router, prefix="/vendedores", tags=["Vendedores"])
app.include_router(example_router, prefix="/example", tags=["Example"])

# ROTAS FIXAS
@app.get("/", description="Mensagem de boas-vindas da API.")
async def read_root():
    return {"message": "Bem-vindo à API de Tratamento de Dados!"}

@app.get("/health", description="Verifica a saúde da API.")
async def health_check():
    return {"status": "ok"}
