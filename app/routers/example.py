from fastapi import APIRouter
from app.services import process_example_data
from app.schemas import ExampleData, ProcessedExampleData

router = APIRouter()

@router.get("/example", description="Endpoint de exemplo que retorna uma mensagem simples.")
async def read_example():
    """Endpoint de exemplo que retorna uma mensagem simples."""
    return {"message": "This is an example endpoint."}

@router.post("/example", description="Endpoint de exemplo que processa dados recebidos.")
async def create_example(data: ExampleData):
    """Endpoint de exemplo que processa dados recebidos."""
    processed_data = process_example_data(data)
    return {"message": "Data processed successfully.", "data": processed_data}