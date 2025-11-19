from pydantic import BaseModel

class VendedorRaw(BaseModel):
    seller_id: str | None = None
    seller_zip_code_prefix: str | None = None
    seller_city: str | None = None
    seller_state: str | None = None
