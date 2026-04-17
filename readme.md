# Pipeline de Dados para E-commerce (Data Lakehouse)

Este projeto é uma simulação de um ambiente real de Engenharia de Dados, focado em extrair, transformar e modelar dados de um e-commerce para consumo por ferramentas de Business Intelligence.

O objetivo principal foi construir uma infraestrutura de dados moderna, orquestrada e escalável, utilizando o conceito de Data Lakehouse e a Arquitetura Medalhão (Medallion Architecture).

## Arquitetura do Projeto

O fluxo de dados foi desenhado em três camadas lógicas, garantindo a rastreabilidade e a qualidade da informação do início ao fim do processo:

*   **Camada Bronze (Ingestão Bruta):**
    Os dados são extraídos de uma API externa (Fake Store API) simulando o sistema transacional do e-commerce. Nesta camada, os dados são salvos localmente em seu formato original, garantindo o histórico exato do que foi recebido, sem nenhuma alteração.

*   **Camada Silver (Limpeza e Padronização):**
    Os dados brutos são lidos, limpos e tipados corretamente utilizando Python. Valores nulos são tratados e os arquivos resultantes são salvos no formato colunar Parquet, o que garante alta compressão e performance para leituras futuras.

*   **Camada Gold (Modelagem Analítica):**
    Os dados limpos são cruzados (joins entre clientes, produtos e pedidos) e as regras de negócio são aplicadas. O resultado é ingerido em um banco de dados analítico baseado em arquivos (DuckDB), criando um Data Warehouse local pronto para ser consumido por relatórios e dashboards.

## Tecnologias Utilizadas

A stack foi escolhida com base em ferramentas amplamente utilizadas no mercado atual de dados:

*   **Linguagem:** Python
*   **Orquestração:** Apache Airflow
*   **Infraestrutura e Deploy:** Docker e Astro CLI (Astronomer)
*   **Processamento e Armazenamento Temporário:** Pandas e formato Parquet
*   **Banco de Dados Analítico:** DuckDB

## Estrutura do Repositório

*   `dags/`: Contém o script Python (`pipeline_ecommerce.py`) que define o fluxo e a ordem de execução das tarefas no Airflow.
*   `include/scripts/`: Abriga os scripts Python individuais responsáveis pela lógica de cada etapa (extração na Bronze, tratamento na Silver e modelagem na Gold).
*   `include/data/`: Diretório ignorado no versionamento, utilizado localmente pelo container do Airflow para armazenar os arquivos Parquet e o banco DuckDB.
*   `Dockerfile` e `requirements.txt`: Arquivos de configuração da imagem Docker e dependências do ambiente Python.

## Como executar o projeto localmente

Para rodar este pipeline na sua máquina, você precisará ter o Docker Desktop e o Astro CLI instalados.

1.  Clone este repositório para a sua máquina local.
2.  Abra o terminal na pasta raiz do projeto.
3.  Inicie a infraestrutura do Airflow executando o comando:
    ```bash
    astro dev start
    ```
4.  Após a inicialização (os containers do Postgres, Scheduler e Webserver estarão rodando), acesse a interface do Airflow no seu navegador, geralmente em `http://localhost:8080`.
5.  O usuário e senha padrão são `admin` / `admin`.
6.  Na interface, ative a DAG correspondente ao pipeline do e-commerce e clique em "Trigger DAG" para acompanhar a execução das tarefas.

## Próximos Passos (Consumo)

Ao finalizar a execução da DAG com sucesso, o banco de dados analítico estará disponível na pasta da camada Gold. Qualquer ferramenta de visualização de dados moderna, como Power BI ou Metabase, pode se conectar diretamente ao arquivo do DuckDB para a criação de painéis e extração de insights de negócio.