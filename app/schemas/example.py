from pydantic import BaseModel

class ExampleData(BaseModel):
    id: int
    name: str
    value: float

class ProcessedExampleData(BaseModel):
    id: int
    name: str
    value: float
    processed: bool