import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from app.services.vendedor_service import tratar_vendedores


# ----------------------------
# CONFIGURAÇÃO
# ----------------------------
SERVICE_ACCOUNT_FILE = "app/service_account.json"

ORIGIN_SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
ORIGIN_TAB = "vendedores"

DEST_SHEET_ID = "1a_uZP-cxopmCDw-z-OCxumzUYxIv27UUkNFBb8tdVKs"
DEST_TAB = "vendedores_dw"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def autenticar():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return gspread.authorize(creds)


def ler_origem(client):
    ws = client.open_by_key(ORIGIN_SHEET_ID).worksheet(ORIGIN_TAB)
    return pd.DataFrame(ws.get_all_records())


def escrever_destino(client, df):
    ws = client.open_by_key(DEST_SHEET_ID).worksheet(DEST_TAB)
    ws.clear()
    ws.update([df.columns.tolist()] + df.astype(str).values.tolist())


def full_load_vendedores():
    print("🔵 FULL LOAD — vendedores")

    client = autenticar()

    df_raw = ler_origem(client)
    print(f"→ {len(df_raw)} registros encontrados.")

    lista_tratada = tratar_vendedores(df_raw.to_dict(orient="records"))
    df_tratado = pd.DataFrame(lista_tratada)

    print("→ Gravando DW...")
    escrever_destino(client, df_tratado)

    print("🏁 FULL LOAD de vendedores concluído!")
    return df_tratado


def tratar_ultima_linha_vendedores():
    client = autenticar()
    ws = client.open_by_key(ORIGIN_SHEET_ID).worksheet(ORIGIN_TAB)

    cabecalho = ws.row_values(1)
    ultima_linha = ws.row_values(ws.row_count)

    raw = dict(zip(cabecalho, ultima_linha))

    vendedor = tratar_vendedores([raw])[0]
    return vendedor
