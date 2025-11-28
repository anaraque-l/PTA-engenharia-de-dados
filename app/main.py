from fastapi import FastAPI
import uvicorn


from app.routers.produto_router import router as produto_router
from app.routers.vendedor_routes import router as vendedor_router
from app.routers.itenspedidos_routes import router as itenspedidos_router
from app.routers import pedidos_router


from app.fullload.full_load_produtos import full_load_produtos
from app.fullload.full_load_pedidos import full_load_pedidos
from app.fullload.full_load_vendedores import full_load_vendedores
from app.fullload.full_load_itens_pedidos import full_load_itens_pedidos  
from app.fullload.full_load_carregar import carregar_ids_dimensoes




app = FastAPI(
    title="API de Tratamento de Dados - Desafio 1",
    description="API que recebe dados brutos, os trata e os devolve limpos.",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    print("🚀 FULL LOAD iniciado...")
    full_load_pedidos()
    full_load_vendedores()  
    full_load_produtos()
    pedidos_ids, produtos_ids, vendedores_ids = carregar_ids_dimensoes()
    full_load_itens_pedidos(pedidos_ids, produtos_ids, vendedores_ids)




# REGISTRO DOS ROUTERS
app.include_router(produto_router, prefix="/produto", tags=["Produtos"])
app.include_router(vendedor_router, prefix="/vendedores", tags=["Vendedores"])
app.include_router(itenspedidos_router, prefix="/itens-pedidos", tags=["ItensPedidos"])
app.include_router(pedidos_router.router, prefix="/pedidos", tags=["Pedidos"])




# ROTAS FIXAS
@app.get("/", description="Mensagem de boas-vindas da API.")
async def read_root():
    return {"message": "Bem-vindo à API de Tratamento de Dados!"}


@app.get("/health", description="Verifica a saúde da API.")
async def health_check():
    return {"status": "ok"}