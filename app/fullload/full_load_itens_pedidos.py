import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from app.services.itenspedidos_service import limpar_itens


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

ORIGIN_SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
ORIGIN_TAB = "itens_pedidos"

DEST_SHEET_ID = "1a_uZP-cxopmCDw-z-OCxumzUYxIv27UUkNFBb8tdVKs"
DEST_TAB = "itens_pedidos_dw"

SERVICE_ACCOUNT_FILE = "app/service_account.json"


# ---------------------------
# Função de Autenticação do Google Cloud
# ---------------------------

def autenticar():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client


# ---------------------------
# Função de leitura da planilha de origem
# ---------------------------

def ler_origem(client):
    ws = client.open_by_key(ORIGIN_SHEET_ID).worksheet(ORIGIN_TAB)
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df

# ---------------------------
# Função de escrita na planilha destino
# ---------------------------

def escrever_destino(client, df):
    ws = client.open_by_key(DEST_SHEET_ID).worksheet(DEST_TAB)
    ws.clear()  # apaga tudo antes de escrever

    ws.update([df.columns.tolist()] + df.astype(str).values.tolist())

# -------------------------
# Função para dividir em chunks
# -------------------------

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

# -------------------------
# Enviar um chunk para a API com retry
# -------------------------

def processar_chunk(chunk, pedidos_ids, produtos_ids, vendedores_ids):

    # Filtrar linhas vazias
    # Remove linhas totalmente vazias ou com todos valores None/NaN/""
    chunk_filtrado = [
        row for row in chunk
        if any(v not in (None, "", float("nan")) for v in row.values())
    ]

    # Se o chunk filtrado ficar vazio, não devemos enviar nada
    if not chunk_filtrado:
        print("Chunk ignorado porque está vazio após filtragem.")
        return []
    
    try:
        resp = limpar_itens(chunk, pedidos_ids, produtos_ids, vendedores_ids)

       
        return resp

    except Exception as e:

        

        print("Falha definitiva ao enviar o chunk.")
        return []

# -------------------------
# Função geral
# -------------------------

def tratar_itens_em_chunks(df: pd.DataFrame, pedidos_ids, produtos_ids, vendedores_ids,chunk_size=5000):

    print(f"Iniciando tratamento via API ({len(df)} linhas)...")
    payload = df.to_dict(orient="records")

    resultados = []
    total_chunks = (len(payload) // chunk_size) + 1

    for i, chunk in enumerate(chunk_list(payload, chunk_size), start=1):
        print(f"Enviando chunk {i}/{total_chunks} ({len(chunk)} registros)...")

        dados_tratados = processar_chunk(chunk, pedidos_ids, produtos_ids, vendedores_ids)

        print(f"   API retornou {len(dados_tratados)} itens limpos\n")

        resultados.extend(dados_tratados)

    print(f"🏁 Finalizado. Total retornado: {len(resultados)}")

    return pd.DataFrame(resultados)

def full_load_itens_pedidos(pedidos_ids, produtos_ids, vendedores_ids):
    
    client = autenticar()

    print("Lendo dados da planilha origem...")
    df_origem = ler_origem(client)

    print("Enviando itens para a API...")
    df_tratado = tratar_itens_em_chunks(df_origem, pedidos_ids, produtos_ids, vendedores_ids)

    print("Escrevendo itens tratados na planilha destino...")
    escrever_destino(client, df_tratado)

    print("Concluído com sucesso!")