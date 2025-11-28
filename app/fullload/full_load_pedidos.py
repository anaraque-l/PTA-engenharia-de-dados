import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


from app.services.pedidos_service import tratar_pedidos




# ------------------------------------------------------
# CONFIGURAÇÃO DOS SHEETS
# ------------------------------------------------------


SERVICE_ACCOUNT_FILE = "app/service_account.json"


# mesma planilha usada nos outros datasets
ORIGIN_SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
ORIGIN_TAB = "pedidos"


DEST_SHEET_ID = "1a_uZP-cxopmCDw-z-OCxumzUYxIv27UUkNFBb8tdVKs"
DEST_TAB = "pedidos_dw"


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]




# ------------------------------------------------------
# AUTENTICAÇÃO
# ------------------------------------------------------


def autenticar():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return gspread.authorize(creds)




# ------------------------------------------------------
# LEITURA DA PLANILHA DE ORIGEM
# ------------------------------------------------------


def ler_origem_pedidos(client):
    ws = client.open_by_key(ORIGIN_SHEET_ID).worksheet(ORIGIN_TAB)
    data = ws.get_all_records()
    return pd.DataFrame(data)




# ------------------------------------------------------
# ESCRITA NA PLANILHA DESTINO (DW)
# ------------------------------------------------------


def escrever_destino_pedidos(client, df):
    ws = client.open_by_key(DEST_SHEET_ID).worksheet(DEST_TAB)
    ws.clear()  # apaga tudo antes de escrever
    ws.update([df.columns.tolist()] + df.astype(str).values.tolist())




# ------------------------------------------------------
# FULL LOAD — RODADO AUTOMATICAMENTE NO DEPLOY
# ------------------------------------------------------


def full_load_pedidos():
    print("🔵 Iniciando FULL LOAD de pedidos...")


    client = autenticar()


    print("→ Lendo planilha de origem...")
    df_origem = ler_origem_pedidos(client)


    print(f"→ {len(df_origem)} registros encontrados.")


    print("→ Tratando pedidos com o service...")
    lista_raw = df_origem.to_dict(orient="records")
    lista_tratada = tratar_pedidos(lista_raw)


    df_tratado = pd.DataFrame(lista_tratada)


    print("→ Gravando pedidos limpos na DW...")
    escrever_destino_pedidos(client, df_tratado)


    print("🏁 FULL LOAD de pedidos concluído com sucesso!")


    return df_tratado




# ------------------------------------------------------
# INCREMENTAL — TRATAR APENAS A ÚLTIMA LINHA
# ------------------------------------------------------


def tratar_ultima_linha_pedidos():
    client = autenticar()
    ws = client.open_by_key(ORIGIN_SHEET_ID).worksheet(ORIGIN_TAB)


    cabecalho = ws.row_values(1)
    ultima_linha = ws.row_values(ws.row_count)


    raw = dict(zip(cabecalho, ultima_linha))


    limpo = tratar_pedidos([raw])[0]


    return limpo
