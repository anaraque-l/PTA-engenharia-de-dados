from pydantic import BaseModel

class VendedorRaw(BaseModel):
    seller_id: str | None = None
    seller_zip_code_prefix: str | None = None
    seller_city: str | None = None
    seller_state: str | None = None

class VendedorClean(BaseModel):
    seller_id: str
    seller_zip_code_prefix: int
    seller_city: str
    seller_state: str