from fullload_service import tratar_itens_via_api_em_chunks
from fullload_service import autenticar
from fullload_service import ler_origem
from fullload_service import escrever_destino

client = autenticar()

print("Lendo dados da planilha origem...")
df_origem = ler_origem(client)

print("Enviando itens para a API...")
df_tratado = tratar_itens_via_api_em_chunks(df_origem)

print("Escrevendo itens tratados na planilha destino...")
escrever_destino(client, df_tratado)

print("Concluído com sucesso!")
