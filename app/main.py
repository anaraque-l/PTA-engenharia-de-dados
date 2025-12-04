from fastapi import FastAPI
import uvicorn


from app.routers.produto_router import router as produto_router
from app.routers.vendedor_routes import router as vendedor_router
from app.routers.itenspedidos_routes import router as itenspedidos_router
from app.routers.pedidos_router import router as pedidos_router
from app.cache_ids import carregar_ids





app = FastAPI(
    title="API de Tratamento de Dados - Desafio 1",
    description="API que recebe dados brutos, os trata e os devolve limpos.",
    version="1.0.0"
)

pedidos_ids = set()
produtos_ids = set()
vendedores_ids = set()

@app.on_event("startup")
def startup_event():
    global pedidos_ids, produtos_ids, vendedores_ids
    
    print("🔵 Carregando IDs do Google Sheets...")
    pedidos_ids, produtos_ids, vendedores_ids = carregar_ids()
    print(f"🟢 IDs carregados: {len(pedidos_ids)} pedidos, {len(produtos_ids)} produtos, {len(vendedores_ids)} vendedores.")



# REGISTRO DOS ROUTERS
app.include_router(produto_router, prefix="/produto", tags=["Produtos"])
app.include_router(vendedor_router, prefix="/vendedores", tags=["Vendedores"])
app.include_router(itenspedidos_router, prefix="/itens-pedidos", tags=["ItensPedidos"])
app.include_router(pedidos_router, prefix="/pedidos", tags=["Pedidos"])




# ROTAS FIXAS
@app.get("/", description="Mensagem de boas-vindas da API.")
async def read_root():
    return {"message": "Bem-vindo à API de Tratamento de Dados!"}


@app.get("/health", description="Verifica a saúde da API.")
async def health_check():
    return {"status": "ok"}