import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
SERVICE_ACCOUNT_FILE = "app/service_account.json"

ABA_PEDIDOS = "pedidos"
ABA_PRODUTOS = "produtos"
ABA_VENDEDORES = "vendedores"


def autenticar():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return gspread.authorize(creds)


def carregar_ids():
    """Lê IDs das três tabelas reais e retorna 3 sets."""
    
    client = autenticar()

    # ---- pedidos ----
    ws_ped = client.open_by_key(SHEET_ID).worksheet(ABA_PEDIDOS)
    pedidos_raw = ws_ped.get_all_records()
    pedidos_ids = {str(l["order_id"]).strip() for l in pedidos_raw if l.get("order_id")}

    # ---- produtos ----
    ws_prod = client.open_by_key(SHEET_ID).worksheet(ABA_PRODUTOS)
    produtos_raw = ws_prod.get_all_records()
    produtos_ids = {str(l["product_id"]).strip() for l in produtos_raw if l.get("product_id")}

    # ---- vendedores ----
    ws_vend = client.open_by_key(SHEET_ID).worksheet(ABA_VENDEDORES)
    vendedores_raw = ws_vend.get_all_records()
    vendedores_ids = {str(l["seller_id"]).strip() for l in vendedores_raw if l.get("seller_id")}

    return pedidos_ids, produtos_ids, vendedores_ids
