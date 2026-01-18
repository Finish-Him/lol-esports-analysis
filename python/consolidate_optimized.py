#!/usr/bin/env python3
"""
Script otimizado para consolidar dados de LoL Esports em chunks
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
print("CONSOLIDAÇÃO OTIMIZADA DE DADOS DE LOL ESPORTS")
print("=" * 80)

# Processar e salvar em partes
teams_dfs = []
players_dfs = []

print("\nProcessando arquivos...")
for csv_file in csv_files:
    year = os.path.basename(csv_file).split("_")[0]
    print(f"  {year}...", end=" ", flush=True)
    
    df = pd.read_csv(csv_file, low_memory=False)
    df['source_file'] = year
    
    # Separar times e jogadores
    teams_dfs.append(df[df['position'] == 'team'].copy())
    players_dfs.append(df[df['position'] != 'team'].copy())
    
    print(f"{len(df):,} linhas")
    del df
    gc.collect()

# Consolidar times
print("\nConsolidando dados de times...")
df_teams = pd.concat(teams_dfs, ignore_index=True)
del teams_dfs
gc.collect()
print(f"  Total: {len(df_teams):,} registros")

# Salvar times
print("  Salvando...")
df_teams.to_parquet(os.path.join(output_dir, "lol_esports_teams.parquet"), index=False)
print(f"  -> lol_esports_teams.parquet")

# Consolidar jogadores
print("\nConsolidando dados de jogadores...")
df_players = pd.concat(players_dfs, ignore_index=True)
del players_dfs
gc.collect()
print(f"  Total: {len(df_players):,} registros")

# Salvar jogadores
print("  Salvando...")
df_players.to_parquet(os.path.join(output_dir, "lol_esports_players.parquet"), index=False)
print(f"  -> lol_esports_players.parquet")

# Criar dataset de partidas
print("\nCriando dataset de partidas...")

# Colunas essenciais para partidas
match_cols = ['gameid', 'league', 'year', 'split', 'patch', 'date', 'gamelength', 'side',
              'teamname', 'teamid', 'result', 'kills', 'deaths', 'dragons', 'barons', 
              'towers', 'firstblood', 'firstdragon', 'firstbaron', 'firsttower', 'firstherald',
              'ban1', 'ban2', 'ban3', 'ban4', 'ban5', 'goldat10', 'goldat15', 'goldat20',
              'xpat10', 'xpat15', 'xpat20', 'csat10', 'csat15', 'csat20']

available_cols = [c for c in match_cols if c in df_teams.columns]
df_teams_slim = df_teams[available_cols].copy()

# Separar por lado
blue = df_teams_slim[df_teams_slim['side'] == 'Blue'].copy()
red = df_teams_slim[df_teams_slim['side'] == 'Red'].copy()

# Renomear colunas
merge_keys = ['gameid', 'league', 'year', 'split', 'patch', 'date', 'gamelength']
blue_rename = {c: f'blue_{c}' for c in blue.columns if c not in merge_keys}
red_rename = {c: f'red_{c}' for c in red.columns if c not in merge_keys}

blue = blue.rename(columns=blue_rename)
red = red.rename(columns=red_rename)

# Merge
df_matches = blue.merge(red, on=merge_keys, how='inner')
df_matches['winner'] = df_matches['blue_result'].apply(lambda x: 'Blue' if x == 1 else 'Red')

print(f"  Total de partidas: {len(df_matches):,}")
df_matches.to_parquet(os.path.join(output_dir, "lol_esports_matches.parquet"), index=False)
print(f"  -> lol_esports_matches.parquet")

del blue, red, df_teams_slim
gc.collect()

# Criar dataset de draft
print("\nCriando dataset de draft...")

# Picks por partida
picks_cols = ['gameid', 'side', 'position', 'champion']
picks = df_players[picks_cols].copy()

blue_picks = picks[picks['side'] == 'Blue'].pivot_table(
    index='gameid', columns='position', values='champion', aggfunc='first'
).reset_index()
blue_picks.columns = ['gameid'] + [f'blue_pick_{c}' for c in blue_picks.columns[1:]]

red_picks = picks[picks['side'] == 'Red'].pivot_table(
    index='gameid', columns='position', values='champion', aggfunc='first'
).reset_index()
red_picks.columns = ['gameid'] + [f'red_pick_{c}' for c in red_picks.columns[1:]]

# Bans
ban_cols = ['gameid', 'side', 'ban1', 'ban2', 'ban3', 'ban4', 'ban5']
bans = df_teams[[c for c in ban_cols if c in df_teams.columns]].copy()

blue_bans = bans[bans['side'] == 'Blue'].drop(columns=['side'])
blue_bans.columns = ['gameid'] + [f'blue_{c}' for c in blue_bans.columns[1:]]

red_bans = bans[bans['side'] == 'Red'].drop(columns=['side'])
red_bans.columns = ['gameid'] + [f'red_{c}' for c in red_bans.columns[1:]]

# Merge draft
df_draft = blue_picks.merge(red_picks, on='gameid', how='outer')
df_draft = df_draft.merge(blue_bans, on='gameid', how='left')
df_draft = df_draft.merge(red_bans, on='gameid', how='left')

# Adicionar info da partida
match_info = df_teams[['gameid', 'league', 'year', 'patch', 'date']].drop_duplicates()
df_draft = df_draft.merge(match_info, on='gameid', how='left')

df_draft.to_parquet(os.path.join(output_dir, "lol_esports_draft.parquet"), index=False)
print(f"  -> lol_esports_draft.parquet")

# Criar índices
print("\nCriando índices...")

# Times
teams_idx = df_teams[['teamname', 'teamid', 'league']].drop_duplicates()
teams_idx.to_csv(os.path.join(output_dir, "teams_index.csv"), index=False)
print(f"  -> teams_index.csv ({len(teams_idx)} times)")

# Jogadores
players_idx = df_players[['playername', 'playerid', 'teamname', 'position']].drop_duplicates()
players_idx.to_csv(os.path.join(output_dir, "players_index.csv"), index=False)
print(f"  -> players_index.csv ({len(players_idx)} jogadores)")

# Campeões
champions = df_players['champion'].dropna().unique()
pd.DataFrame({'champion': sorted(champions)}).to_csv(
    os.path.join(output_dir, "champions_index.csv"), index=False
)
print(f"  -> champions_index.csv ({len(champions)} campeões)")

# Ligas
leagues = df_teams['league'].unique()
pd.DataFrame({'league': sorted(leagues)}).to_csv(
    os.path.join(output_dir, "leagues_index.csv"), index=False
)
print(f"  -> leagues_index.csv ({len(leagues)} ligas)")

# Patches
patches = df_teams['patch'].dropna().unique()
pd.DataFrame({'patch': sorted(patches, key=lambda x: str(x))}).to_csv(
    os.path.join(output_dir, "patches_index.csv"), index=False
)
print(f"  -> patches_index.csv ({len(patches)} patches)")

print("\n" + "=" * 80)
print("CONSOLIDAÇÃO CONCLUÍDA")
print("=" * 80)

# Listar arquivos
print("\nArquivos criados:")
for f in sorted(os.listdir(output_dir)):
    path = os.path.join(output_dir, f)
    size = os.path.getsize(path)
    if size > 1024 * 1024:
        print(f"  {f}: {size / (1024*1024):.1f} MB")
    else:
        print(f"  {f}: {size / 1024:.1f} KB")
