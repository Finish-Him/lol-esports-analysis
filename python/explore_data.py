#!/usr/bin/env python3
"""
Script para análise exploratória inicial dos dados de LoL Esports
"""

import pandas as pd
import os
import glob
from datetime import datetime

# Configurações
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Diretório dos dados
data_dir = "/home/ubuntu/upload/"
output_dir = "/home/ubuntu/lol_prediction_project/data/"

# Listar todos os arquivos CSV
csv_files = sorted(glob.glob(os.path.join(data_dir, "*_LoL_esports_match_data_from_OraclesElixir.csv")))

print("=" * 80)
print("ANÁLISE EXPLORATÓRIA DOS DADOS DE LOL ESPORTS (2014-2026)")
print("=" * 80)

# Analisar estrutura de cada arquivo
all_dfs = []
file_info = []

for csv_file in csv_files:
    year = os.path.basename(csv_file).split("_")[0]
    print(f"\n--- Analisando arquivo {year} ---")
    
    try:
        df = pd.read_csv(csv_file, low_memory=False)
        
        info = {
            'ano': year,
            'linhas': len(df),
            'colunas': len(df.columns),
            'tamanho_mb': os.path.getsize(csv_file) / (1024 * 1024)
        }
        file_info.append(info)
        
        print(f"  Linhas: {len(df):,}")
        print(f"  Colunas: {len(df.columns)}")
        
        # Adicionar coluna de ano para referência
        df['source_year'] = int(year)
        all_dfs.append(df)
        
    except Exception as e:
        print(f"  ERRO ao ler arquivo: {e}")

# Resumo geral
print("\n" + "=" * 80)
print("RESUMO GERAL DOS ARQUIVOS")
print("=" * 80)
info_df = pd.DataFrame(file_info)
print(info_df.to_string(index=False))
print(f"\nTotal de linhas: {info_df['linhas'].sum():,}")
print(f"Tamanho total: {info_df['tamanho_mb'].sum():.2f} MB")

# Verificar se todos os arquivos têm as mesmas colunas
print("\n" + "=" * 80)
print("ANÁLISE DE COLUNAS")
print("=" * 80)

# Pegar colunas do arquivo mais recente como referência
reference_cols = set(all_dfs[-1].columns)
print(f"\nColunas no arquivo mais recente (2026): {len(reference_cols) - 1}")  # -1 para source_year

# Verificar diferenças entre anos
for i, df in enumerate(all_dfs):
    year = file_info[i]['ano']
    cols = set(df.columns)
    missing = reference_cols - cols
    extra = cols - reference_cols
    if missing or extra:
        print(f"\n{year}:")
        if missing:
            print(f"  Colunas faltando: {missing}")
        if extra:
            print(f"  Colunas extras: {extra}")

# Analisar estrutura detalhada do arquivo mais recente
print("\n" + "=" * 80)
print("ESTRUTURA DETALHADA (ARQUIVO 2026)")
print("=" * 80)
df_recent = all_dfs[-1]
print("\nColunas disponíveis:")
for i, col in enumerate(sorted(df_recent.columns)):
    dtype = df_recent[col].dtype
    non_null = df_recent[col].notna().sum()
    pct = (non_null / len(df_recent)) * 100
    print(f"  {i+1:3d}. {col:40s} | {str(dtype):15s} | {pct:5.1f}% preenchido")

# Analisar colunas-chave
print("\n" + "=" * 80)
print("ANÁLISE DE COLUNAS-CHAVE")
print("=" * 80)

key_columns = ['gameid', 'league', 'patch', 'side', 'position', 'playername', 
               'teamname', 'champion', 'result', 'kills', 'deaths', 'assists',
               'dragons', 'barons', 'towers', 'gamelength', 'date']

for col in key_columns:
    if col in df_recent.columns:
        print(f"\n{col}:")
        print(f"  Valores únicos: {df_recent[col].nunique()}")
        print(f"  Valores nulos: {df_recent[col].isna().sum()}")
        if df_recent[col].dtype == 'object':
            print(f"  Exemplos: {df_recent[col].dropna().head(5).tolist()}")
        else:
            print(f"  Min: {df_recent[col].min()}, Max: {df_recent[col].max()}")

# Salvar informações de estrutura
print("\n" + "=" * 80)
print("SALVANDO INFORMAÇÕES")
print("=" * 80)

# Salvar lista completa de colunas
with open(os.path.join(output_dir, "column_list.txt"), "w") as f:
    f.write("LISTA COMPLETA DE COLUNAS DO DATASET\n")
    f.write("=" * 50 + "\n\n")
    for col in sorted(df_recent.columns):
        f.write(f"{col}\n")

print("Informações salvas em column_list.txt")
print("\nAnálise concluída!")
