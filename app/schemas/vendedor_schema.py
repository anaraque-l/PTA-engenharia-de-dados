from pydantic import BaseModel

class VendedorRaw(BaseModel):
    seller_id: str | int | float | None = None
    seller_zip_code_prefix: str | int | float | None = None
    seller_city: str | int | float | None = None
    seller_state: str | int | float | None = None


class VendedorClean(BaseModel):
    seller_id: str
    seller_zip_code_prefix: int
    seller_city: str
    seller_state: str
