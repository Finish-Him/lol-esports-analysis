#!/usr/bin/env python3
"""
Script para consolidar e armazenar todos os dados de LoL Esports de forma permanente
"""

import pandas as pd
import os
import glob
import gc
from datetime import datetime

# Diretórios
data_dir = "/home/ubuntu/upload/"
output_dir = "/home/ubuntu/lol_prediction_project/data/"
os.makedirs(output_dir, exist_ok=True)

csv_files = sorted(glob.glob(os.path.join(data_dir, "*_LoL_esports_match_data_from_OraclesElixir.csv")))

print("=" * 80)
print("CONSOLIDAÇÃO E ARMAZENAMENTO DE DADOS DE LOL ESPORTS")
print("=" * 80)
print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Carregar todos os arquivos
all_dfs = []
print("\nCarregando arquivos...")

for csv_file in csv_files:
    year = os.path.basename(csv_file).split("_")[0]
    print(f"  {year}...", end=" ")
    df = pd.read_csv(csv_file, low_memory=False)
    df['source_file'] = year
    all_dfs.append(df)
    print(f"{len(df):,} linhas")

# Concatenar todos os dados
print("\nConcatenando dados...")
df_all = pd.concat(all_dfs, ignore_index=True)
print(f"Total de linhas: {len(df_all):,}")

# Liberar memória
del all_dfs
gc.collect()

# Separar dados de jogadores e times
print("\nSeparando dados de jogadores e times...")
df_players = df_all[df_all['position'] != 'team'].copy()
df_teams = df_all[df_all['position'] == 'team'].copy()

print(f"  Registros de jogadores: {len(df_players):,}")
print(f"  Registros de times: {len(df_teams):,}")

# Salvar datasets consolidados
print("\nSalvando datasets consolidados...")

# 1. Dataset completo (todos os registros)
print("  1. Salvando dataset completo...")
df_all.to_parquet(os.path.join(output_dir, "lol_esports_all_data.parquet"), index=False)
print(f"     -> lol_esports_all_data.parquet ({os.path.getsize(os.path.join(output_dir, 'lol_esports_all_data.parquet')) / (1024*1024):.1f} MB)")

# 2. Dataset de times (agregado por partida)
print("  2. Salvando dataset de times...")
df_teams.to_parquet(os.path.join(output_dir, "lol_esports_teams.parquet"), index=False)
print(f"     -> lol_esports_teams.parquet ({os.path.getsize(os.path.join(output_dir, 'lol_esports_teams.parquet')) / (1024*1024):.1f} MB)")

# 3. Dataset de jogadores
print("  3. Salvando dataset de jogadores...")
df_players.to_parquet(os.path.join(output_dir, "lol_esports_players.parquet"), index=False)
print(f"     -> lol_esports_players.parquet ({os.path.getsize(os.path.join(output_dir, 'lol_esports_players.parquet')) / (1024*1024):.1f} MB)")

# 4. Criar dataset de partidas (uma linha por partida com informações de ambos os times)
print("  4. Criando dataset de partidas...")

# Separar times por lado
blue_teams = df_teams[df_teams['side'] == 'Blue'].copy()
red_teams = df_teams[df_teams['side'] == 'Red'].copy()

# Renomear colunas para merge
blue_cols = {col: f'blue_{col}' if col not in ['gameid', 'league', 'year', 'split', 'patch', 'date', 'gamelength'] else col 
             for col in blue_teams.columns}
red_cols = {col: f'red_{col}' if col not in ['gameid', 'league', 'year', 'split', 'patch', 'date', 'gamelength'] else col 
            for col in red_teams.columns}

blue_teams = blue_teams.rename(columns=blue_cols)
red_teams = red_teams.rename(columns=red_cols)

# Merge para criar dataset de partidas
merge_cols = ['gameid', 'league', 'year', 'split', 'patch', 'date', 'gamelength']
df_matches = blue_teams.merge(red_teams, on=merge_cols, how='inner')

# Adicionar coluna de vencedor
df_matches['winner'] = df_matches.apply(
    lambda x: 'Blue' if x['blue_result'] == 1 else 'Red', axis=1
)

print(f"     Total de partidas: {len(df_matches):,}")
df_matches.to_parquet(os.path.join(output_dir, "lol_esports_matches.parquet"), index=False)
print(f"     -> lol_esports_matches.parquet ({os.path.getsize(os.path.join(output_dir, 'lol_esports_matches.parquet')) / (1024*1024):.1f} MB)")

# 5. Criar dataset de draft (picks e bans por partida)
print("  5. Criando dataset de draft...")

# Colunas de draft
ban_cols = ['ban1', 'ban2', 'ban3', 'ban4', 'ban5']
pick_cols = ['champion']  # picks estão nos dados de jogadores

# Extrair picks dos jogadores
picks_blue = df_players[df_players['side'] == 'Blue'].groupby('gameid').agg({
    'champion': list,
    'position': list
}).reset_index()
picks_blue.columns = ['gameid', 'blue_picks', 'blue_positions']

picks_red = df_players[df_players['side'] == 'Red'].groupby('gameid').agg({
    'champion': list,
    'position': list
}).reset_index()
picks_red.columns = ['gameid', 'red_picks', 'red_positions']

# Extrair bans
bans_blue = df_teams[df_teams['side'] == 'Blue'][['gameid'] + ban_cols].copy()
bans_blue.columns = ['gameid'] + [f'blue_{col}' for col in ban_cols]

bans_red = df_teams[df_teams['side'] == 'Red'][['gameid'] + ban_cols].copy()
bans_red.columns = ['gameid'] + [f'red_{col}' for col in ban_cols]

# Merge draft data
df_draft = picks_blue.merge(picks_red, on='gameid', how='outer')
df_draft = df_draft.merge(bans_blue, on='gameid', how='left')
df_draft = df_draft.merge(bans_red, on='gameid', how='left')

# Adicionar informações da partida
match_info = df_teams[['gameid', 'league', 'year', 'patch', 'date']].drop_duplicates()
df_draft = df_draft.merge(match_info, on='gameid', how='left')

df_draft.to_parquet(os.path.join(output_dir, "lol_esports_draft.parquet"), index=False)
print(f"     -> lol_esports_draft.parquet ({os.path.getsize(os.path.join(output_dir, 'lol_esports_draft.parquet')) / (1024*1024):.1f} MB)")

# 6. Criar índices e metadados
print("  6. Criando índices e metadados...")

# Lista de times únicos
teams_list = df_teams[['teamname', 'teamid']].drop_duplicates()
teams_list.to_csv(os.path.join(output_dir, "teams_index.csv"), index=False)

# Lista de jogadores únicos
players_list = df_players[['playername', 'playerid', 'teamname']].drop_duplicates()
players_list.to_csv(os.path.join(output_dir, "players_index.csv"), index=False)

# Lista de campeões únicos
champions_list = df_players['champion'].dropna().unique()
pd.DataFrame({'champion': sorted(champions_list)}).to_csv(
    os.path.join(output_dir, "champions_index.csv"), index=False
)

# Lista de ligas
leagues_list = df_all['league'].unique()
pd.DataFrame({'league': sorted(leagues_list)}).to_csv(
    os.path.join(output_dir, "leagues_index.csv"), index=False
)

# Lista de patches
patches_list = df_all['patch'].dropna().unique()
pd.DataFrame({'patch': sorted(patches_list, key=lambda x: str(x))}).to_csv(
    os.path.join(output_dir, "patches_index.csv"), index=False
)

print("\n" + "=" * 80)
print("CONSOLIDAÇÃO CONCLUÍDA")
print("=" * 80)

# Listar arquivos criados
print("\nArquivos criados:")
for f in sorted(os.listdir(output_dir)):
    size = os.path.getsize(os.path.join(output_dir, f))
    if size > 1024 * 1024:
        print(f"  {f}: {size / (1024*1024):.1f} MB")
    else:
        print(f"  {f}: {size / 1024:.1f} KB")

print("\nDados armazenados com sucesso!")
