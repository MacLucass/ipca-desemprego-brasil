"""
Script de extração de dados IPCA e Desemprego via API SIDRA do IBGE
Autor: Lucas Corrêa
Data: Janeiro/2026
"""

import requests
import pandas as pd


# URLs das APIs do IBGE (SIDRA)
IPCA_URL = "https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/63/p/all"
DESEMPREGO_URL = "https://apisidra.ibge.gov.br/values/t/6381/n1/all/v/4099/p/all"


def baixar_ipca():
    """
    Baixa dados de IPCA mensal do Brasil via API SIDRA.
    Salva resultado em CSV na pasta data/raw/
    """
    print("Baixando dados de IPCA...")
    
    response = requests.get(IPCA_URL)
    response.raise_for_status()
    dados = response.json()

    # A primeira linha é cabeçalho, o resto são os dados
    df = pd.DataFrame(dados[1:])

    # Renomear colunas principais
    df = df.rename(columns={
        "D1C": "brasil",
        "D2C": "ano_mes",
        "V": "ipca"
    })

    # Converter coluna de valor para numérico
    df["ipca"] = pd.to_numeric(df["ipca"], errors="coerce")

    # Salvar em CSV
    df.to_csv("../data/raw/ipca_brasil.csv", index=False, encoding="utf-8-sig")
    print(f"✓ Arquivo ipca_brasil.csv salvo com {len(df)} registros!")


def baixar_desemprego():
    """
    Baixa dados de taxa de desocupação (desemprego) do Brasil via API SIDRA.
    Salva resultado em CSV na pasta data/raw/
    """
    print("Baixando dados de desemprego...")
    
    response = requests.get(DESEMPREGO_URL)
    response.raise_for_status()
    dados = response.json()

    # Ignora a primeira linha (cabeçalho bruto)
    df = pd.DataFrame(dados[1:])

    # Renomeia colunas principais
    df = df.rename(columns={
        "D1C": "brasil",
        "D2C": "ano_mes",
        "V": "desemprego"
    })

    # Converter coluna de valor para numérico
    df["desemprego"] = pd.to_numeric(df["desemprego"], errors="coerce")

    # Salva CSV
    df.to_csv("../data/raw/desemprego_brasil.csv", index=False, encoding="utf-8-sig")
    print(f"✓ Arquivo desemprego_brasil.csv salvo com {len(df)} registros!")


if __name__ == "__main__":
    print("=" * 50)
    print("Extração de dados IPCA x Desemprego - IBGE")
    print("=" * 50)
    
    baixar_ipca()
    baixar_desemprego()
    
    print("\n✓ Extração concluída com sucesso!")
