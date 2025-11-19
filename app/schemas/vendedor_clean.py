from pydantic import BaseModel

class VendedorClean(BaseModel):
    seller_id: str
    seller_zip_code_prefix: int
    seller_city: str
    seller_state: str
