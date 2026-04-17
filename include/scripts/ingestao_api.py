import requests
import json
import os
from datetime import datetime

os.makedirs('include/data/bronze', exist_ok=True)

API_BASE_URL = "https://fakestoreapi.com"
ENDPOINTS = {
    'clientes': f"{API_BASE_URL}/users",
    'produtos': f"{API_BASE_URL}/products",
    'pedidos': f"{API_BASE_URL}/carts"
}

def extrair_dados_api():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando extração da API Fake Store...")
    
    for nome_tabela, url in ENDPOINTS.items():
        print(f"Buscando {nome_tabela} de: {url}")
        
        try:
            resposta = requests.get(url)
            resposta.raise_for_status() 
            
            dados = resposta.json()
            
            caminho_arquivo = f"include/data/bronze/{nome_tabela}_raw.json"
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
                
            print(f"Sucesso! {len(dados)} registros salvos em {caminho_arquivo}\n")
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar na API para {nome_tabela}: {e}\n")

if __name__ == "__main__":
    extrair_dados_api()
    print("(Ingestão Bronze) concluída com sucesso!")