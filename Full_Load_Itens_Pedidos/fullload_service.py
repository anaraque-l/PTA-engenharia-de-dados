import time
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

ORIGIN_SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
ORIGIN_TAB = "itens_pedidos"

DEST_SHEET_ID = "1a_uZP-cxopmCDw-z-OCxumzUYxIv27UUkNFBb8tdVKs"
DEST_TAB = "itens_pedidos_dw"

SERVICE_ACCOUNT_FILE = "Full_Load_Itens_Pedidos/service_account.json"

API_URL = "https://pta-engenharia-de-dados-3.onrender.com/itens-pedidos/limpar-itens-pedidos"

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

def processar_chunk(chunk, tentativa=1):

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
        resp = requests.post(API_URL, json=chunk, timeout=60)

        if resp.status_code != 200:
            raise Exception(f"Erro HTTP {resp.status_code}: {resp.text}")

        try:
            data = resp.json()
        except Exception:
            raise Exception("Resposta inválida da API (não é JSON).")

        # resposta tem que ser lista — mas fazemos normalização
        if isinstance(data, dict):
            data = list(data.values())

        if not isinstance(data, list):
            raise Exception("API retornou um formato inesperado.")

        return data

    except Exception as e:
        print(f"[ERRO] Tentativa {tentativa} falhou: {e}")

        if tentativa < 3:
            time.sleep(2)
            return processar_chunk(chunk, tentativa + 1)

        print("Falha definitiva ao enviar o chunk.")
        return []

# -------------------------
# Função geral
# -------------------------

def tratar_itens_via_api_em_chunks(df: pd.DataFrame, chunk_size=5000):

    print(f"Iniciando tratamento via API ({len(df)} linhas)...")
    payload = df.to_dict(orient="records")

    resultados = []
    total_chunks = (len(payload) // chunk_size) + 1

    for i, chunk in enumerate(chunk_list(payload, chunk_size), start=1):
        print(f"Enviando chunk {i}/{total_chunks} ({len(chunk)} registros)...")

        dados_tratados = processar_chunk(chunk)

        print(f"   API retornou {len(dados_tratados)} itens limpos\n")

        resultados.extend(dados_tratados)

    print(f"🏁 Finalizado. Total retornado: {len(resultados)}")

    return pd.DataFrame(resultados)