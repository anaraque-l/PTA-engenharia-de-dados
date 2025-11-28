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

Sobre o Projeto

Este projeto foi desenvolvido para o Processo de Treinamento de Área (PTA) do CITi, com foco em engenharia de dados. Ele inclui uma API construída com FastAPI, utilizando boas práticas de desenvolvimento e uma estrutura modular para facilitar a manutenção e a escalabilidade. O objetivo principal do projeto é construir uma pipeline completa que consiga ser acessada via uma API.

Este projeto implementa uma arquitetura de ETL (Extract, Transform, Load) para dados de e-commerce, utilizando FastAPI para higienização de dados e n8n para orquestração de fluxos, com persistência em planilhas Google.

🛠 Tecnologias Utilizadas

Linguagem: Python

API Framework: FastAPI

Orquestração: n8n

Integração: Google Cloud Platform (Google Sheets API)

⚙️ Tratamento de Dados (Backend)

O núcleo do tratamento de dados reside na API, responsável por garantir a integridade das informações antes do armazenamento. A arquitetura segue o padrão de Schemas (Pydantic) para validação e Services para regras de negócio.

📦 Pedidos

Localização: app/schemas/pedidos_schema.py e app/services/pedidos_service.py

Modelagem:

PedidosRaw (Entrada): Trata todos os campos como string. Otimizado para leitura de dados brutos (CSV/Planilhas) onde a tipagem não é garantida.

PedidosClean (Saída): Define tipos estritos (ex: datetime para datas, string para IDs).

Lógica de Processamento:

Sanitização: Remoção de espaços em branco extras (trimming).

Conversão: Campos de data convertidos de string para datetime.

Validação: order_purchase_timestamp é obrigatório. Se for nulo/inválido, a linha é ignorada (ValueError). Outros campos com falha recebem None.

🛒 Produtos

Localização: app/schemas/produto_schema.py e app/services/produto_service.py

Modelagem:

ProdutosRaw: Recebe dados em formato misto (string, int, nulos).

ProdutosClean: Restringe os tipos conforme o schema do Data Warehouse.

Lógica de Processamento:

Categoria (product_category_name): Trim, substituição de espaços por underscore (_) e preenchimento de vazios com "indefinido".

Dados Numéricos: Conversão inicial para float. Cálculo da mediana de cada coluna numérica para preenchimento de valores nulos (Inputação de dados).

Tipagem Final: Conversão de floats para inteiros onde aplicável.

👥 Vendedores e Itens

Seguem a estrutura padrão de Schemas (vendedor_schema.py, itenspedidos_schema.py) e Services correspondentes, garantindo a tipagem e limpeza antes da carga.

🔗 API Router

O endpoint (app/routers/) atua como controlador central:

Recebe uma lista de objetos Raw.

Itera sobre os dados aplicando o Service de tratamento.

Filtra registros inválidos.

Retorna apenas a lista de objetos processados com sucesso (Clean).

🔄 Workflows de Automação (n8n & Scripts)

Fluxo: Vendedores

Full Load (Carga Inicial): Leitura integral, tratamento via API, conversão final para string e deduplicação de IDs. Criação de nova aba "Limpa" no Sheets.

Incremental (Atualização): Acionado via trigger de novas linhas (lê as últimas 5). Utiliza lógica de Upsert: Se ID existe, atualiza; se não, insere.

Fluxo: Produtos

Full Load: Gatilho manual. Leitura integral "quebrada" em grupos de 200 itens para otimização de memória da automação. Escrita na página dedicada do Warehouse.

Incremental: Acionado a cada 15 minutos. Processa em lotes de 200 itens com tratamento via API (Mock/Produção).

Fluxos: Itens Pedidos e Pedidos

Ambos possuem estratégias definidas para Full Load e Carga Incremental seguindo os padrões de arquitetura do projeto.

📂 Estrutura de Pastas

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


Como Instalar

Certifique-se de que o Python e o Docker Desktop estão instalados em sua máquina.

Clone o repositório:

git clone [https://github.com/CITi-UFPE/PTA-engenharia-de-dados.git](https://github.com/CITi-UFPE/PTA-engenharia-de-dados.git)


Entre na pasta do projeto:

cd PTA-engenharia-de-dados


Como Rodar

Usando Docker

Certifique-se de que o Docker Desktop está em execução.

Suba os serviços com o Docker Compose:

docker-compose up --build


Acesse a aplicação em seu navegador no endereço:

http://localhost:8000


Para acessar a documentação interativa da API (Swagger UI), vá para:

http://localhost:8000/docs


Localmente

Certifique-se de que esteja no diretório principal.

Instale as dependências:

pip install -r ./requirements.txt


Execute o projeto:

uvicorn app.main:app


Acesse a aplicação em seu navegador no endereço:

http://localhost:8000


Para acessar a documentação interativa da API (Swagger UI), vá para:

http://localhost:8000/docs


Contato

CITi UFPE - contato@citi.org.br

João Pedro Bezerra, Líder de Dados em 2025.2 - jpbmtl@cin.ufpe.br