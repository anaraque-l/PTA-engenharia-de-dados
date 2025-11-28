<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados">
    <img src="https://ci3.googleusercontent.com/mail-sig/AIorK4zWbC3U-G_vTTZE6rUQqJjzL8u7WNZjzhEaYi9z7slJn8vNhgnFVootxjm377GVCdPGY_F64WolHmGJ" alt="Logo" width="180px">
  </a>

  <h3 align="center">PTA Engenharia de Dados</h3>

  <p align="center">
  Este projeto foi criado em 2025.2 com a proposta de trazer a frente de engenharia de dados para o Processo de Treinamento de Área (PTA) do CITi. Ele foi desenvolvido com base em práticas modernas de engenharia de dados e tem como objetivo capacitar tecnicamente as pessoas aspirantes, alinhando-se às demandas atuais da empresa.

   
    <br />
    <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados/issues">Report Bug</a>
    ·
    <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Tabela de Conteúdo</h2></summary>
  <ol>
    <li><a href="#sobre-o-projeto">Sobre o Projeto</a></li>
    
    <li><a href="#como-instalar">Como Instalar</a></li>
    <li><a href="#como-rodar">Como Rodar</a></li>
    <li><a href="#contato">Contato</a></li>
  </ol>
</details>

<br/>

## Sobre o Projeto
<br/>

Este projeto foi desenvolvido para o Processo de Treinamento de Área (PTA) do CITi, com foco em engenharia de dados. Ele inclui uma API construída com FastAPI, utilizando boas práticas de desenvolvimento e uma estrutura modular para facilitar a manutenção e a escalabilidade. O objetivo principal do projeto é construir uma pipeline completa que consiga ser acessada via uma API.

Este projeto implementa uma arquitetura de ETL (Extract, Transform, Load) para dados de e-commerce, utilizando FastAPI para higienização de dados e n8n para orquestração de fluxos, com persistência em planilhas Google.

🛠 Tecnologias Utilizadas Linguagem: Python

API Framework: FastAPI

Orquestração: n8n

Integração: Google Cloud Platform (Google Sheets API)

Tratamento de Dados (Backend) O núcleo do tratamento de dados reside na API, responsável por garantir a integridade das informações antes do armazenamento.
Pedidos
Modelagem de Classes (Schemas) - Padronização de Entradas e Saídas
Localização: app/schemas/pedidos_schema.py

PedidosRaw (Entrada): Trata todos os campos como string. Otimizado para leitura de dados brutos (CSV/Planilhas) onde a tipagem não é garantida.

PedidosClean (Saída): Define tipos estritos (ex: datetime para datas, string para IDs).

Lógica de Processamento
Localização: app/services/pedidos_service.py

A função de tratamento processa a tabela linha a linha, aplicando as seguintes regras:

Sanitização de Texto: Remoção de espaços em branco extras (trimming) em campos textuais.

Conversão de Tipos: Campos de data convertidos de string para datetime. Validação do campo obrigatório order_purchase_timestamp.

Tratamento de Erros: Se order_purchase_timestamp for nulo/inválido: Lança ValueError e a linha é ignorada (bloco try/except). Outros campos com falha de conversão: Recebem valor None (nulo), mantendo o objeto válido.

Vendedores
Modelagem de Classes (Schemas) - Padronização de Entradas e Saídas
Localização: app/schemas/vendedor_schema.py

Lógica de Processamento
Localização: app/services/vendedor_service.py

Produtos
Modelagem de Classes (Schemas) - Padronização de Entradas e Saídas
Localização: app/schemas/produto_schema.py

ProdutosRaw (Entrada): Recebe dados no formato desejável (que pode ser string, int ou outro) ou nulos (None). ProdutosClean (Saída): Restringe os tipos de dados, de acordo com o desejável.

Lógica de Processamento
Localização: app/services/produto_service.py

A função de tratamento processa a tabela linha a linha, aplicando as seguintes regras:

Sanitização de texto (coluna 'product_category_name'): remoção de espaços em branco extras, substituição de espaços em branco entre termos por underscore (_) e preenchimento dos espaços em branco por "indefinido".

Sanitização dos dados numéricos: conversão para float de todas as colunas que dizem respeito a dados numéricos; cálculo da mediana de cada uma delas e preenchimento dos espaços em branco com a respectiva mediana.

Conversão de tipagem: transformação dos valores numéricos que devem ser tratados como inteiros, pois, pelo passo anterior, eles eram float.

Por fim, são criadas novas colunas, com os dados corrigidos.

Itens pedidos
Modelagem de Classes (Schemas) - Padronização de Entradas e Saídas
Localização: app/schemas/itenspedidos_schema.py

Lógica de Processamento
Localização: app/schemas/itenspedidos_service.py

API Router (comum a todas as categorias)
Localização: app/routers/

O endpoint recebe uma lista de objetos PedidosRaw e retorna uma lista de PedidosClean. Itera sobre os dados recebidos. Aplica a função de tratamento. Filtra registros inválidos (erros de campos obrigatórios). Retorna apenas a lista de objetos processados com sucesso.

Workflows de Automação (n8n & Scripts)
Fluxo: Vendedores
Estratégia "Full Load" (Carga Inicial):
Leitura integral da planilha bruta. Tratamento via API (Mock/Produção). Conversão final de todos os campos para string (padronização de persistência). Deduplicação: Remoção de IDs repetidos. Escrita: Google Sheets: Criação de nova aba/planilha "Limpa". Notificação via Email após conclusão.

Estratégia Incremental (Atualização):
Acionado via trigger de novas linhas na planilha, carregando apenas as últimas 5 linhas (margem de segurança). Padronização para string. Lógica de Upsert (Update/Insert): Verifica se o ID já existe no destino. Se existir: Atualiza o registro. Se não existir: Insere novo registro. Notificação via Email.

Fluxo: Produtos (Products)
Estratégia "Full Load" (Carga Inicial):
Gatilho manual (clique em "executar workflow"). Leitura integral da planilha bruta. "Quebra" em grupos de 200, para facilitar à automação realizar as tarefas sem comprometer sua limitada memória. Tratamento via API (Mock/Produção). Escrita em página do Warehouse dedicada à categoria em qeustão. Notificação via Email.

Estratégia Incremental (Atualização):
Acionado a cada 15 minutos. "Quebra" em grupos de 200, para facilitar à automação realizar as tarefas sem comprometer sua limitada memória. Tratamento via API (Mock/Produção). Escrita em página do Warehouse dedicada à categoria em qeustão. Notificação via Email.

Fluxo: Itens Pedidos
Estratégia "Full Load" (Carga Inicial):
Estratégia Incremental (Atualização):
Fluxo: Pedidos
Estratégia "Full Load" (Carga Inicial):
Estratégia Incremental (Atualização):

### Estrutura de Pastas

```text
projeto-etl/
│
├── app/
│   ├── main.py                  # Ponto de entrada da aplicação (Entrypoint)
│   │
│   ├── routers/                 # Endpoints da API (Controladores)
│   │   ├── pedidos_router.py    # Recebe requisições de Pedidos
│   │   ├── produtos_router.py   # Recebe requisições de Produtos
│   │   └── ...
│   │
│   ├── services/                # Regras de Negócio e Limpeza (Lógica ETL)
│   │   ├── pedidos_service.py   # Sanitização e conversão de Pedidos
│   │   ├── produtos_service.py  # Tratamento de nulos e medianas de Produtos
│   │   └── ...
│   │
│   └── schemas/                 # Modelagem de Dados (Pydantic)
│       ├── pedidos_schema.py    # Define PedidosRaw e PedidosClean
│       ├── produtos_schema.py   # Define ProdutosRaw e ProdutosClean
│       └── ...
│
├── requirements.txt             # Dependências do projeto
└── README.md                    # Documentação

<br/>

## Como Instalar
<br/>

1. Certifique-se de que o **Python** e o **Docker Desktop** estão instalados em sua máquina.

2. Clone o repositório:

   ```sh
   git clone https://github.com/CITi-UFPE/PTA-engenharia-de-dados.git
   ```

3. Entre na pasta do projeto:

   ```sh
   cd PTA-engenharia-de-dados
   ```

<br/>

## Como Rodar

### Usando Docker
<br/>

1. Certifique-se de que o Docker Desktop está em execução.

2. Suba os serviços com o Docker Compose:

   ```sh
   docker-compose up --build
   ```

3. Acesse a aplicação em seu navegador no endereço:

   ```
   http://localhost:8000
   ```

4. Para acessar a documentação interativa da API (Swagger UI), vá para:

   ```
   http://localhost:8000/docs
   ```

<br/>

### Localmente
<br/>

1. Certifique-se de que esteja no diretório principal

2. Instale as dependências: 
    ```
    pip install -r ./requirements.txt
    ```

3. Execute o projeto: 
    ```
    uvicorn app.main:app
    ```

4. Acesse a aplicação em seu navegador no endereço:

   ```
   http://localhost:8000
   ```

5. Para acessar a documentação interativa da API (Swagger UI), vá para:

   ```
   http://localhost:8000/docs
   ```

<br/>


## Contato
<br/>

- [CITi UFPE](https://github.com/CITi-UFPE) - contato@citi.org.br
- [João Pedro Bezerra](https://github.com/jpbezera), Líder de Dados em 2025.2 - jpbmtl@cin.ufpe.br