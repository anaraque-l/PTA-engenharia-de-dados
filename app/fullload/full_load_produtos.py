import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from app.services.produto_service import tratar_produtos


# ------------------------------------------------------
# CONFIGURAÇÃO DOS SHEETS
# ------------------------------------------------------

SERVICE_ACCOUNT_FILE = "app/service_account.json"

# mesma origem que você usou para itens
ORIGIN_SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
ORIGIN_TAB = "produtos"

# mesma DW que você usa para itens, só muda a aba
DEST_SHEET_ID = "1a_uZP-cxopmCDw-z-OCxumzUYxIv27UUkNFBb8tdVKs"
DEST_TAB = "PRODUTOS"

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
# LEITURA DA ORIGEM
# ------------------------------------------------------

def ler_origem_produtos(client):
    ws = client.open_by_key(ORIGIN_SHEET_ID).worksheet(ORIGIN_TAB)
    data = ws.get_all_records()
    return pd.DataFrame(data)


# ------------------------------------------------------
# ESCRITA DA DESTINO
# ------------------------------------------------------

def escrever_destino_produtos(client, df):
    ws = client.open_by_key(DEST_SHEET_ID).worksheet(DEST_TAB)

    ws.clear()   # limpa antes de escrever
    ws.update([df.columns.tolist()] + df.astype(str).values.tolist())


# ------------------------------------------------------
# FULL LOAD COMPLETO (rodar no deploy)
# ------------------------------------------------------

def full_load_produtos():
    print("🔵 Iniciando FULL LOAD de produtos...")

    client = autenticar()

    print("→ Lendo a planilha origem...")
    df_origem = ler_origem_produtos(client)

    print(f"→ {len(df_origem)} registros encontrados.")

    print("→ Tratando produtos usando service...")
    lista_raw = df_origem.to_dict(orient="records")
    df_tratado = pd.DataFrame(tratar_produtos(lista_raw))

    print("→ Escrevendo produtos limpos na DW...")
    escrever_destino_produtos(client, df_tratado)

    print("🏁 FULL LOAD de produtos concluído!")

    return df_tratado


# ------------------------------------------------------
# INCREMENTAL — ÚLTIMA LINHA
# ------------------------------------------------------

def tratar_ultima_linha_produtos():
    client = autenticar()
    ws = client.open_by_key(ORIGIN_SHEET_ID).worksheet(ORIGIN_TAB)

    cabecalho = ws.row_values(1)
    ultima_linha = ws.row_values(ws.row_count)

    raw = dict(zip(cabecalho, ultima_linha))

    # seu service trata lista → por isso embrulhamos em []
    limpo = tratar_produtos([raw])[0]

    return limpo
