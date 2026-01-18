#!/usr/bin/env python3
"""
Script para análise detalhada e consolidação dos dados de LoL Esports
"""

import pandas as pd
import os
import glob
import json
from collections import Counter

# Configurações
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Diretório dos dados
data_dir = "/home/ubuntu/upload/"
output_dir = "/home/ubuntu/lol_prediction_project/data/"

# Carregar todos os arquivos
csv_files = sorted(glob.glob(os.path.join(data_dir, "*_LoL_esports_match_data_from_OraclesElixir.csv")))

print("Carregando todos os arquivos...")
all_dfs = []
for csv_file in csv_files:
    year = os.path.basename(csv_file).split("_")[0]
    df = pd.read_csv(csv_file, low_memory=False)
    df['source_file_year'] = int(year)
    all_dfs.append(df)
    print(f"  {year}: {len(df):,} linhas")

# Concatenar todos os dados
print("\nConcatenando dados...")
df_all = pd.concat(all_dfs, ignore_index=True)
print(f"Total de linhas: {len(df_all):,}")

# Análise de estrutura
print("\n" + "=" * 80)
print("ANÁLISE DETALHADA DO DATASET CONSOLIDADO")
print("=" * 80)

# Identificar tipos de linhas (jogador vs time)
print("\n--- Tipos de Registros ---")
position_counts = df_all['position'].value_counts()
print(position_counts)

# Separar dados de jogadores e times
df_players = df_all[df_all['position'] != 'team'].copy()
df_teams = df_all[df_all['position'] == 'team'].copy()

print(f"\nRegistros de jogadores: {len(df_players):,}")
print(f"Registros de times: {len(df_teams):,}")

# Análise de partidas
print("\n--- Análise de Partidas ---")
n_games = df_all['gameid'].nunique()
print(f"Total de partidas únicas: {n_games:,}")

# Partidas por ano
games_by_year = df_teams.groupby('year')['gameid'].nunique()
print("\nPartidas por ano:")
print(games_by_year.to_string())

# Análise de ligas
print("\n--- Análise de Ligas ---")
leagues = df_all['league'].unique()
print(f"Total de ligas: {len(leagues)}")
print("\nTop 20 ligas por número de partidas:")
league_games = df_teams.groupby('league')['gameid'].nunique().sort_values(ascending=False)
print(league_games.head(20).to_string())

# Análise de patches
print("\n--- Análise de Patches ---")
patches = df_all['patch'].dropna().unique()
print(f"Total de patches únicos: {len(patches)}")
print("\nExemplos de patches:")
print(sorted(df_all['patch'].dropna().unique())[:20])

# Análise de times
print("\n--- Análise de Times ---")
teams = df_all['teamname'].unique()
print(f"Total de times únicos: {len(teams)}")

# Análise de jogadores
print("\n--- Análise de Jogadores ---")
players = df_players['playername'].dropna().unique()
print(f"Total de jogadores únicos: {len(players)}")

# Análise de campeões
print("\n--- Análise de Campeões ---")
champions = df_players['champion'].dropna().unique()
print(f"Total de campeões únicos: {len(champions)}")

# Análise de variáveis-alvo potenciais
print("\n--- Variáveis-Alvo Potenciais ---")
target_vars = ['result', 'gamelength', 'kills', 'deaths', 'dragons', 'barons', 
               'towers', 'firstblood', 'firstdragon', 'firstbaron', 'firsttower']

for var in target_vars:
    if var in df_teams.columns:
        print(f"\n{var}:")
        print(f"  Valores únicos: {df_teams[var].nunique()}")
        print(f"  Nulos: {df_teams[var].isna().sum()} ({df_teams[var].isna().mean()*100:.1f}%)")
        if df_teams[var].dtype in ['int64', 'float64']:
            print(f"  Min: {df_teams[var].min()}, Max: {df_teams[var].max()}, Média: {df_teams[var].mean():.2f}")

# Análise de dados de draft (bans e picks)
print("\n--- Análise de Draft ---")
ban_cols = [col for col in df_all.columns if 'ban' in col.lower()]
pick_cols = [col for col in df_all.columns if 'pick' in col.lower()]
print(f"Colunas de ban: {ban_cols}")
print(f"Colunas de pick: {pick_cols}")

# Verificar disponibilidade de dados de draft
if ban_cols:
    sample = df_teams[ban_cols].head(10)
    print("\nExemplo de dados de ban:")
    print(sample.to_string())

# Análise temporal
print("\n--- Análise Temporal ---")
if 'date' in df_all.columns:
    df_all['date_parsed'] = pd.to_datetime(df_all['date'], errors='coerce')
    date_range = df_all['date_parsed'].agg(['min', 'max'])
    print(f"Período dos dados: {date_range['min']} até {date_range['max']}")

# Análise de completude por ano
print("\n--- Completude de Dados por Ano ---")
important_cols = ['result', 'gamelength', 'dragons', 'barons', 'towers', 
                  'firstblood', 'firstdragon', 'firstbaron', 'patch']

completeness = []
for year in sorted(df_teams['year'].unique()):
    year_data = df_teams[df_teams['year'] == year]
    row = {'ano': year, 'partidas': year_data['gameid'].nunique()}
    for col in important_cols:
        if col in year_data.columns:
            row[col] = f"{(1 - year_data[col].isna().mean()) * 100:.1f}%"
    completeness.append(row)

completeness_df = pd.DataFrame(completeness)
print(completeness_df.to_string(index=False))

# Salvar estatísticas em JSON
stats = {
    'total_rows': len(df_all),
    'total_games': n_games,
    'total_players': len(players),
    'total_teams': len(teams),
    'total_champions': len(champions),
    'total_leagues': len(leagues),
    'total_patches': len(patches),
    'years_covered': sorted(df_all['year'].unique().tolist()),
    'columns': list(df_all.columns),
    'games_by_year': games_by_year.to_dict(),
    'top_leagues': league_games.head(30).to_dict()
}

with open(os.path.join(output_dir, "dataset_stats.json"), "w") as f:
    json.dump(stats, f, indent=2, default=str)

print("\n" + "=" * 80)
print("Estatísticas salvas em dataset_stats.json")
print("=" * 80)
