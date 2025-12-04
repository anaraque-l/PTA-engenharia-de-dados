import time
import logging
import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

SHEET_ID = "1eXQ7RUogkIlCzaVzpCJ0DCfdCgS9MbEH3uBih5x7GXg"
SERVICE_ACCOUNT_FILE = "app/service_account.json"

ABA_PEDIDOS = "pedidos"
ABA_PRODUTOS = "produtos"
ABA_VENDEDORES = "vendedores"

MAX_TENTATIVAS = 4
ESPERA = 20  # segundos


def autenticar():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return gspread.authorize(creds)


def carregar_ids():
    """Lê IDs das três tabelas reais com retry, espera e leitura otimizada."""
    
    tentativas = 0

    while tentativas < MAX_TENTATIVAS:
        try:
            tentativas += 1
            logger.info(f"[cache_ids] Tentativa {tentativas}/{MAX_TENTATIVAS} para carregar IDs...")

            # 1. Autentica apenas uma vez
            client = autenticar()

            # 2. Abre a planilha uma única vez
            sheet = client.open_by_key(SHEET_ID)

            # ---- pedidos ----
            ws_ped = sheet.worksheet(ABA_PEDIDOS)
            pedidos_raw = ws_ped.get_all_records()
            pedidos_ids = {str(l["order_id"]).strip() for l in pedidos_raw if l.get("order_id")}

            # ---- produtos ----
            ws_prod = sheet.worksheet(ABA_PRODUTOS)
            produtos_raw = ws_prod.get_all_records()
            produtos_ids = {str(l["product_id"]).strip() for l in produtos_raw if l.get("product_id")}

            # ---- vendedores ----
            ws_vend = sheet.worksheet(ABA_VENDEDORES)
            vendedores_raw = ws_vend.get_all_records()
            vendedores_ids = {str(l["seller_id"]).strip() for l in vendedores_raw if l.get("seller_id")}

            # Se chegou aqui: SUCESSO
            logger.info(
                f"[cache_ids] Carregados: {len(pedidos_ids)} pedidos, "
                f"{len(produtos_ids)} produtos, {len(vendedores_ids)} vendedores."
            )
            return pedidos_ids, produtos_ids, vendedores_ids

        except Exception as e:
            logger.error(f"[cache_ids] ERRO ao carregar IDs: {e}")

            if tentativas < MAX_TENTATIVAS:
                logger.warning(f"[cache_ids] Aguardando {ESPERA} segundos antes de tentar novamente...")
                time.sleep(ESPERA)
            else:
                logger.critical("[cache_ids] Todas as tentativas falharam. Abortando startup.")
                raise
