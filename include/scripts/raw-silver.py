import pandas as pd
import json
import os

# Garante que a pasta silver existe
os.makedirs('include/data/silver', exist_ok=True)

def processar_clientes():
    print("Processando Clientes...")
    with open('include/data/bronze/clientes_raw.json', 'r', encoding="utf-8") as f:
        dados = json.load(f)
    
    # pd.json_normalize achata os dicionários aninhados (ex: address.city)
    df_clientes = pd.json_normalize(dados)
    
    # Selecionando e renomeando colunas importantes
    colunas = {
        'id': 'id_cliente',
        'email': 'email',
        'username': 'usuario',
        'name.firstname': 'nome',
        'name.lastname': 'sobrenome',
        'address.city': 'cidade',
        'address.street': 'rua'
    }
    df_clientes = df_clientes[list(colunas.keys())].rename(columns=colunas)
    
    # Salvando na camada Silver em Parquet
    df_clientes.to_parquet('include/data/silver/clientes_silver.parquet', index=False)
    print(f"Clientes processados: {len(df_clientes)} linhas.")

def processar_produtos():
    print("Processando Produtos...")
    with open('include/data/bronze/produtos_raw.json', 'r', encoding="utf-8") as f:
        dados = json.load(f)
        
    df_produtos = pd.json_normalize(dados)
    
    colunas = {
        'id': 'id_produto',
        'title': 'nome_produto',
        'price': 'preco',
        'category': 'categoria',
        'rating.rate': 'nota_avaliacao',
        'rating.count': 'qtd_avaliacoes'
    }
    df_produtos = df_produtos[list(colunas.keys())].rename(columns=colunas)
    
    # Garantindo que o preço é um número float (decimal)
    df_produtos['preco'] = df_produtos['preco'].astype(float)
    
    df_produtos.to_parquet('include/data/silver/produtos_silver.parquet', index=False)
    print(f"Produtos processados: {len(df_produtos)} linhas.")

def processar_pedidos():
    print("Processando Pedidos (Carts)...")
    with open('include/data/bronze/pedidos_raw.json', 'r', encoding="utf-8") as f:
        dados = json.load(f)
    
    # Aqui o buraco é mais embaixo: temos uma lista de produtos dentro de cada pedido!
    # O record_path='products' vai "explodir" essa lista em várias linhas.
    # O meta=['id', 'userId', 'date'] vai manter a qual pedido/cliente aquele produto pertence.
    df_pedidos = pd.json_normalize(
        dados, 
        record_path='products', 
        meta=['id', 'userId', 'date']
    )
    
    colunas = {
        'id': 'id_pedido',
        'userId': 'id_cliente',
        'date': 'data_pedido',
        'productId': 'id_produto',
        'quantity': 'quantidade'
    }
    df_pedidos = df_pedidos.rename(columns=colunas)
    
    # Convertendo a data de string ISO para datetime real
    df_pedidos['data_pedido'] = pd.to_datetime(df_pedidos['data_pedido'])
    
    # Reordenando as colunas para ficar bonitinho
    df_pedidos = df_pedidos[['id_pedido', 'id_cliente', 'id_produto', 'quantidade', 'data_pedido']]
    
    df_pedidos.to_parquet('include/data/silver/pedidos_silver.parquet', index=False)
    print(f"Pedidos processados: {len(df_pedidos)} linhas.")

if __name__ == "__main__":
    print("Iniciando Transformação para a Camada Silver...")
    processar_clientes()
    processar_produtos()
    processar_pedidos()
    print("Camada Silver finalizada com sucesso! Os dados estão prontos para modelagem.")