# DW E-commerce — Data Lakehouse Local

Simulação de um ambiente real de engenharia de dados para um e-commerce brasileiro. O projeto constrói um **Data Warehouse local** do zero usando Arquitetura Medallion (Bronze → Silver → Gold), orquestrado com Apache Airflow via Astro CLI e armazenado em DuckDB — pronto para consumo por ferramentas de BI.

---

## Arquitetura

```
[Fake Store API]
       │
       ▼
  ┌─────────┐      ┌──────────┐      ┌──────────┐
  │  BRONZE │ ───▶ │  SILVER  │ ───▶ │   GOLD   │
  │  (JSON) │      │ (Parquet)│      │ (DuckDB) │
  └─────────┘      └──────────┘      └──────────┘
       │                  │                 │
  Dado bruto        Limpo e tipado    Modelado e
  sem alteração     formato colunar   pronto pra BI
```

| Camada | Responsabilidade |
|---|---|
| **Bronze** | Ingestão da Fake Store API — salva JSON original sem transformação |
| **Silver** | Limpeza, tipagem e persistência em Parquet com Pandas |
| **Gold** | Joins entre entidades (clientes, produtos, pedidos) + regras de negócio, ingerido no DuckDB |

---

## Stack

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python |
| Orquestração | Apache Airflow (via Astro CLI / Astronomer) |
| Containerização | Docker |
| Processamento | Pandas |
| Formato intermediário | Parquet |
| Banco analítico | DuckDB |
| Fonte de dados | [Fake Store API](https://fakestoreapi.com/) |

---

## Estrutura do Projeto

```
dw-ecommerce/
│
├── dags/
│   └── pipeline_ecommerce.py      # DAG principal — define o fluxo e ordem das tasks
│
├── include/
│   └── scripts/
│       ├── bronze_ingestao.py     # Extração da Fake Store API → JSON
│       ├── silver_tratamento.py   # Limpeza e tipagem → Parquet
│       └── gold_modelagem.py      # Joins e regras de negócio → DuckDB
│
├── Dockerfile                     # Imagem customizada do Airflow
├── packages.txt                   # Dependências de sistema
├── requirements.txt               # Dependências Python
└── .dockerignore
```

> `include/data/` é ignorado no versionamento — gerado localmente pelo container com os arquivos Parquet e o banco DuckDB.

---

## Como Executar

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)

### 1. Clone o repositório

```bash
git clone https://github.com/diasgomess/dw-ecommerce.git
cd dw-ecommerce
```

### 2. Inicie a infraestrutura

```bash
astro dev start
```

O Astro CLI sobe automaticamente os containers do Postgres, Scheduler e Webserver do Airflow.

### 3. Acesse o Airflow

Abra [http://localhost:8080](http://localhost:8080) no navegador.

- **Usuário:** admin
- **Senha:** admin

### 4. Execute o pipeline

Ative a DAG `pipeline_ecommerce` e clique em **Trigger DAG**. Acompanhe o progresso na interface gráfica.

---

## Consumo dos Dados

Ao finalizar a execução da DAG com sucesso, o arquivo DuckDB estará disponível na pasta da camada Gold. Qualquer ferramenta de BI moderna pode se conectar diretamente:

- **Power BI** — via conector DuckDB ou exportação para CSV/Parquet
- **Metabase** — conexão direta com o arquivo `.duckdb`
- **Python/Jupyter** — `import duckdb; con = duckdb.connect('gold/ecommerce.duckdb')`

---

## Próximas Melhorias

| # | Melhoria |
|---|---|
| 1 | Substituir Fake Store API por dados sintéticos com Faker em português |
| 2 | Adicionar camada de qualidade de dados com Great Expectations |
| 3 | Conectar camada Gold ao Power BI com dashboard publicado |
| 4 | Migrar para GCP (GCS + BigQuery + Cloud Composer) |
| 5 | Implementar extração incremental com controle de watermark |

---

## 👤 Autor

**Matheus Gomes** — Trainee de Engenharia de Dados na [Rox Partner](https://www.roxpartner.com.br/)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matheusdgomes/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/diasgomess)
