# 📦 O-MARKET — Pipeline de Engenharia de Dados

Este projeto implementa um **pipeline de engenharia de dados completo** para e-commerce, integrando:

- Coleta  
- Tratamento  
- Integração  
- Persistência  
- Serviços de apoio

A arquitetura garante que os dados sejam:

✔ íntegros  
✔ deduplicados  
✔ consistentes  
✔ auditáveis  
✔ continuamente atualizados

---

## 🛠 Tecnologias Utilizadas

| Componente | Tecnologia |
|---|---|
| Linguagem | Python |
| API | FastAPI |
| Orquestração | n8n |
| Storage | Google Sheets |
| Full Load | Execução local via Uvicorn |
| CI/CD | Branch `feat/fulloaddocker` |
| Monitoração | Logs + E-mail via n8n |

---

## 1. Arquitetura Geral

A arquitetura segue o padrão **Extract → Transform → Load**, com dois modos complementares:

### 🔁 Incremental (produção contínua)
- executado **a cada 15 minutos**
- processa **somente a última linha**
- atualiza o warehouse continuamente

### 🚀 Full Load (carga inicial)
- executado **localmente via uvicorn**
- branch: `feat/fulloaddocker`
- processa **todo o dataset**
- útil para reconstrução e sanity checks

---

## 2. Fluxo High-Level

```
            +-----------------------------+
            |           Usuário           |
            +--------------+--------------+
                           |
                           v
            +-----------------------------+
            |       Coleta (Google)       |
            |   Google Sheets - RAW DATA  |
            +--------------+--------------+
                           |
            +--------------v--------------+
            |             API             |
            |         FastAPI             |
            |  Conversões / Validações    |
            +--------------+--------------+
                           |
            +--------------v--------------+
            |  Warehouse (Google Sheets)  |
            |         Dados Limpos        |
            +--------------+--------------+
                           |
                           v
                     +-----+-----+
                     |   n8n     |
                     | Orquestra |
                     +-----------+
```

---

## 3. Backend (FastAPI)

### 3.1 Estrutura por Domínio

| Domínio | Schemas | Service |
|---|---|---|
| Pedidos | `app/schemas/pedidos_schema.py` | `app/services/pedidos_service.py` |
| Produtos | `app/schemas/produto_schema.py` | `app/services/produto_service.py` |
| Vendedores | `app/schemas/vendedor_schema.py` | `app/services/vendedor_service.py` |
| Itens Pedidos | `app/schemas/itenspedidos_schema.py` | `app/services/itenspedidos_service.py` |

---

### 3.2 Regras de Tratamento

#### Sanitização de texto
- remoção de espaços extras
- padronização
- substituição por underline (`_`)
- preenchimento de nulos com `"indefinido"`

#### Conversão de data
- strings → datetime
- validação de campos obrigatórios

#### Conversão numérica
- strings → float  
- cálculo de **medianas**
- nulos recebem mediana
- reconversão para inteiros quando aplicável

#### Integridade referencial
Em **Itens Pedidos**, IDs são validados contra:
- Produtos
- Pedidos
- Vendedores

Linhas órfãs são descartadas.

### ✨ Extras implementados em **Pedidos**

Além das validações e conversões já descritas, o pipeline de Pedidos inclui regras adicionais que garantem consistência temporal e integridade auditável dos dados:

#### 🧹 Normalização de Timestamp
Todos os campos de data foram convertidos para `datetime` e normalizados para timezone padrão, permitindo análises temporais consistentes.

#### ⏱️ Cálculo Automático de Intervalos
Foram criadas colunas derivadas:
- tempo entre compra e aprovação
- tempo entre aprovação e envio
- tempo total até entrega

Esses indicadores permitem análise de SLA, detecção de gargalos e ranking de performance.

#### 📊 Marcação de Outliers
Pedidos com durações fora da curva recebem:
```
is_outlier = True
```
Esses registros podem ser analisados separadamente para diagnóstico.

#### 🔗 Integridade com Itens
IDs foram validados contra:
- produtos
- vendedores
- itens

Pedidos “órfãos” são descartados, garantindo consistência entre tabelas.

#### 📦 Estrutura preparada para Data Warehouse
Ao final, o dataset contém:
- chave primária única
- timestamps normalizados
- fatos temporais calculados
- flag de outlier

Pronto para agregações, dashboards e relatórios.


---

## 4. Estratégias de Carga

### 🚀 Full Load (Carga Inicial)

- não ocorre no n8n  
- executado **localmente via uvicorn**
- branch: `feat/fulloaddocker`

Responsável por:

- leitura integral dos arquivos brutos  
- limpeza e tipagem  
- deduplicação  
- escrita massiva no warehouse

Usado para:

- primeira construção da base  
- reconstrução completa  
- sanity check de qualidade  

---

### 🔁 Incremental (Produção Contínua)

- executado **a cada 15 minutos**
- captura **somente a última linha**
- custo computacional mínimo

Fluxo:

```
Schedule Trigger (15 min)
        ↓
Read RAW sheet
        ↓
Seleciona apenas a última linha
        ↓
POST → FastAPI (tratamento)
        ↓
Append to clean Warehouse sheet
        ↓
Send Email Notification
```

---

## 5. Workflows n8n

### Pedidos

| Modo | Execução |
|---|---|
| Full Load | via backend (Uvicorn) |
| Incremental | última linha a cada 15 min |

---

### Produtos

| Modo | Execução |
|---|---|
| Full Load | manual, batch 200 |
| Incremental | 15 min, batch 200 |

---

### Vendedores

| Modo | Execução |
|---|---|
| Full Load | manual + dedupe |
| Incremental | upsert (update/insert) |

---

### Itens Pedidos

| Modo | Execução |
|---|---|
| Full Load | via backend |
| Incremental | última linha, rejeita órfãos por FK |

---

## 6. Garantias do Sistema

✔ Tipagem uniforme  
✔ Deduplicação  
✔ Integridade referencial  
✔ Null-safe com medianas  
✔ Erros capturados e logados  
✔ Persistência previsível  
✔ Escalável

---

## 7. Deploy & Execução

### API normal

```
uvicorn app.main:app --reload
```

### Full Load

```
git checkout feat/fulloaddocker
uvicorn app.main:app
```

### n8n

```
docker compose up -d
```

---

## 8. Conclusão

Este pipeline entrega:

✔ Confiabilidade operacional  
✔ Dados limpos e íntegros  
✔ Baixo custo computacional  
✔ Manutenção simples  
✔ Atualização contínua  
✔ Independência entre Full + Incremental  
✔ Arquitetura escalável e sustentável

---

