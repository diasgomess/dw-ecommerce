import duckdb
import os

# Garante que a pasta gold existe
os.makedirs('include/data/gold', exist_ok=True)

def criar_banco_gold():
    print("Iniciando a Modelagem da Camada Gold com DuckDB...")
    
    # Conecta ao arquivo do DuckDB (se não existir, ele cria na hora)
    caminho_db = 'include/data/gold/ecommerce_dw.duckdb'
    con = duckdb.connect(database=caminho_db, read_only=False)
    
    # 1. Cria a Tabela Fato de Vendas (cruzando Pedidos com Produtos)
    print("Criando Fato Vendas...")
    con.execute("""
        CREATE OR REPLACE TABLE fato_vendas AS
        SELECT 
            p.id_pedido,
            p.id_cliente,
            p.id_produto,
            p.quantidade,
            p.data_pedido,
            prod.preco,
            (p.quantidade * prod.preco) AS faturamento_total,
            prod.categoria
        FROM read_parquet('include/data/silver/pedidos_silver.parquet') AS p
        LEFT JOIN read_parquet('include/data/silver/produtos_silver.parquet') AS prod 
            ON p.id_produto = prod.id_produto
    """)
    
    # 2. Cria a Tabela Dimensão de Clientes
    print("Criando Dimensao Clientes...")
    con.execute("""
        CREATE OR REPLACE TABLE dim_clientes AS
        SELECT *
        FROM read_parquet('include/data/silver/clientes_silver.parquet')
    """)
    
    # 3. Cria a Tabela Dimensão de Produtos
    print("Criando Dimensao Produtos...")
    con.execute("""
        CREATE OR REPLACE TABLE dim_produtos AS
        SELECT *
        FROM read_parquet('include/data/silver/produtos_silver.parquet')
    """)
    
    # Validação Básica (Query de teste)
    print("\nResumo do Faturamento Total do nosso E-commerce:")
    resultado = con.execute("SELECT SUM(faturamento_total) as faturamento FROM fato_vendas").df()
    print(resultado)
    
    # 4. Exportação para o Power BI via Pandas
    print("\nExportando views da Gold para CSV (via Pandas)...")
    con.sql("SELECT * FROM fato_vendas").df().to_csv('include/data/gold/fato_vendas.csv', index=False)
    con.sql("SELECT * FROM dim_clientes").df().to_csv('include/data/gold/dim_clientes.csv', index=False)
    con.sql("SELECT * FROM dim_produtos").df().to_csv('include/data/gold/dim_produtos.csv', index=False)
    print("Arquivos CSV prontos na pasta include/data/gold/ para importar no Power BI.")
    
    # Fechando a conexão
    con.close()
    print(f"\nCamada Gold finalizada! Banco salvo em: {caminho_db}")

if __name__ == "__main__":
    criar_banco_gold()