from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configurações padrão da DAG
default_args = {
    'owner': 'engenharia_dados',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Definição da DAG
with DAG(
    'pipeline_ecommerce_diario',
    default_args=default_args,
    description='Pipeline de ETL do E-commerce (Bronze, Silver, Gold)',
    schedule='@daily', 
    catchup=False,
    tags=['ecommerce', 'etl', 'duckdb'],
) as dag:

        # Tarefa 1: Extrair da API (Bronze)
    tarefa_bronze = BashOperator(
        task_id='extracao_bronze',
        bash_command='cd /usr/local/airflow && python include/scripts/ingestao_api.py',
    )

    # Tarefa 2: Limpar e Tipar (Silver)
    tarefa_silver = BashOperator(
        task_id='transformacao_silver',
        bash_command='cd /usr/local/airflow && python include/scripts/raw-silver.py',
    )

    # Tarefa 3: Modelagem e DuckDB (Gold)
    tarefa_gold = BashOperator(
        task_id='modelagem_gold',
        bash_command='cd /usr/local/airflow && python include/scripts/modelagem.py',
    )

    # Definindo a Ordem de Execução (O fluxo da DAG)
    tarefa_bronze >> tarefa_silver >> tarefa_gold