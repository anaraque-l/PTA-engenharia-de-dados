import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SERVICE_ACCOUNT_FILE = "app/service_account.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# IDs das planilhas origem
PEDIDOS_SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
PEDIDOS_TAB = "pedidos"

PRODUTOS_SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
PRODUTOS_TAB = "produtos"

VENDEDORES_SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
VENDEDORES_TAB = "vendedores"


# ------------------------------------------------------
# Autentica Google Sheets
# ------------------------------------------------------
def autenticar_google():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return gspread.authorize(creds)


# ------------------------------------------------------
# Lê uma aba e devolve um DataFrame
# ------------------------------------------------------
def ler_aba(client, sheet_id, tab):
    ws = client.open_by_key(sheet_id).worksheet(tab)
    data = ws.get_all_records()
    return pd.DataFrame(data)


# ------------------------------------------------------
# Carrega os IDs necessários para integridade referencial
# ------------------------------------------------------
def carregar_ids_dimensoes():
    client = autenticar_google()

    # ---- pedidos ----
    df_pedidos = ler_aba(client, PEDIDOS_SHEET_ID, PEDIDOS_TAB)
    pedidos_ids = set(df_pedidos["order_id"].dropna().astype(str))

    # ---- produtos ----
    df_produtos = ler_aba(client, PRODUTOS_SHEET_ID, PRODUTOS_TAB)
    produtos_ids = set(df_produtos["product_id"].dropna().astype(str))

    # ---- vendedores ----
    df_vendedores = ler_aba(client, VENDEDORES_SHEET_ID, VENDEDORES_TAB)
    vendedores_ids = set(df_vendedores["seller_id"].dropna().astype(str))

    return pedidos_ids, produtos_ids, vendedores_ids
