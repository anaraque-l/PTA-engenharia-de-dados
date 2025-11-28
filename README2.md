## Pipeline de Tratamento e Integração da O-MARKET
Este projeto implementa uma arquitetura de ETL (Extract, Transform, Load) para dados de e-commerce, utilizando FastAPI para higienização de dados e n8n para orquestração de fluxos, com persistência em planilhas Google.

🛠 Tecnologias Utilizadas
Linguagem: Python 

API Framework: FastAPI

Orquestração: n8n

Integração: Google Cloud Platform (Google Sheets API)

1. Tratamento de Dados (Backend)
O núcleo do tratamento de dados reside na API, responsável por garantir a integridade das informações antes do armazenamento.

### Pedidos

#### Modelagem de Classes (Schemas) - Padronização de Entradas e Saídas 

Localização: app/schemas/pedidos_schema.py

PedidosRaw (Entrada): Trata todos os campos como string. Otimizado para leitura de dados brutos (CSV/Planilhas) onde a tipagem não é garantida.

PedidosClean (Saída): Define tipos estritos (ex: datetime para datas, string para IDs).

#### Lógica de Processamento

Localização: app/services/pedidos_service.py

A função de tratamento processa a tabela linha a linha, aplicando as seguintes regras:

Sanitização de Texto: Remoção de espaços em branco extras (trimming) em campos textuais.

Conversão de Tipos:
Campos de data convertidos de string para datetime.
Validação do campo obrigatório order_purchase_timestamp.

Tratamento de Erros:
Se order_purchase_timestamp for nulo/inválido: Lança ValueError e a linha é ignorada (bloco try/except).
Outros campos com falha de conversão: Recebem valor None (nulo), mantendo o objeto válido.

### Vendedores

#### Modelagem de Classes (Schemas) - Padronização de Entradas e Saídas 

Localização: app/schemas/vendedor_schema.py

#### Lógica de Processamento

Localização: app/services/vendedor_service.py

### Produtos

#### Modelagem de Classes (Schemas) - Padronização de Entradas e Saídas 

Localização: app/schemas/produto_schema.py

ProdutosRaw (Entrada): Recebe dados no formato desejável (que pode ser string, int ou outro) ou nulos (None). 
ProdutosClean (Saída): Restringe os tipos de dados, de acordo com o desejável.

#### Lógica de Processamento

Localização: app/services/produto_service.py

A função de tratamento processa a tabela linha a linha, aplicando as seguintes regras:

Sanitização de texto (coluna 'product_category_name'): remoção de espaços em branco extras, substituição de espaços em branco entre termos por underscore (_) e preenchimento dos espaços em branco por "indefinido".

Sanitização dos dados numéricos: conversão para float de todas as colunas que dizem respeito a dados numéricos; cálculo da mediana de cada uma delas e preenchimento dos espaços em branco com a respectiva mediana.

Conversão de tipagem: transformação dos valores numéricos que devem ser tratados como inteiros, pois, pelo passo anterior, eles eram float.

Por fim, são criadas novas colunas, com os dados corrigidos.

### Itens pedidos 

#### Modelagem de Classes (Schemas) - Padronização de Entradas e Saídas

Localização: app/schemas/itenspedidos_schema.py

#### Lógica de Processamento

Localização: app/schemas/itenspedidos_service.py


#### API Router (comum a todas as categorias)

Localização: app/routers/

O endpoint recebe uma lista de objetos PedidosRaw e retorna uma lista de PedidosClean.
Itera sobre os dados recebidos.
Aplica a função de tratamento.
Filtra registros inválidos (erros de campos obrigatórios).
Retorna apenas a lista de objetos processados com sucesso.


2. Workflows de Automação (n8n & Scripts)


#### Fluxo: Vendedores 

##### Estratégia "Full Load" (Carga Inicial):

Leitura integral da planilha bruta.
Tratamento via API (Mock/Produção).
Conversão final de todos os campos para string (padronização de persistência).
Deduplicação: Remoção de IDs repetidos.
Escrita:
Google Sheets: Criação de nova aba/planilha "Limpa".
Notificação via Email após conclusão.

##### Estratégia Incremental (Atualização):

Acionado via trigger de novas linhas na planilha, carregando apenas as últimas 5 linhas (margem de segurança).
Padronização para string.
Lógica de Upsert (Update/Insert):
Verifica se o ID já existe no destino.
Se existir: Atualiza o registro.
Se não existir: Insere novo registro.
Notificação via Email.

### Fluxo: Produtos (Products)

##### Estratégia "Full Load" (Carga Inicial):

Gatilho manual (clique em "executar workflow").
Leitura integral da planilha bruta.
"Quebra" em grupos de 200, para facilitar à automação realizar as tarefas sem comprometer sua limitada memória.
Tratamento via API (Mock/Produção).
Escrita em página do Warehouse dedicada à categoria em qeustão.
Notificação via Email.

##### Estratégia Incremental (Atualização):

Acionado a cada 15 minutos.
"Quebra" em grupos de 200, para facilitar à automação realizar as tarefas sem comprometer sua limitada memória.
Tratamento via API (Mock/Produção).
Escrita em página do Warehouse dedicada à categoria em qeustão.
Notificação via Email.

### Fluxo: Itens Pedidos 

##### Estratégia "Full Load" (Carga Inicial):

##### Estratégia Incremental (Atualização):



### Fluxo: Pedidos

##### Estratégia "Full Load" (Carga Inicial):

##### Estratégia Incremental (Atualização):