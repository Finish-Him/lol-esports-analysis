#!/usr/bin/env python3
"""
Script otimizado para análise dos dados de LoL Esports
"""

import pandas as pd
import os
import glob
import json
import gc

# Configurações
pd.set_option('display.max_columns', None)

# Diretórios
data_dir = "/home/ubuntu/upload/"
output_dir = "/home/ubuntu/lol_prediction_project/data/"

# Colunas essenciais para análise inicial
essential_cols = [
    'gameid', 'league', 'year', 'split', 'patch', 'side', 'position',
    'playername', 'teamname', 'champion', 'result', 'gamelength',
    'kills', 'deaths', 'assists', 'dragons', 'barons', 'towers',
    'firstblood', 'firstdragon', 'firstbaron', 'firsttower', 'firstherald',
    'date', 'teamid', 'playerid',
    'ban1', 'ban2', 'ban3', 'ban4', 'ban5'
]

csv_files = sorted(glob.glob(os.path.join(data_dir, "*_LoL_esports_match_data_from_OraclesElixir.csv")))

# Estatísticas gerais
stats = {
    'total_rows': 0,
    'total_games': 0,
    'games_by_year': {},
    'leagues': set(),
    'teams': set(),
    'players': set(),
    'champions': set(),
    'patches': set(),
    'years': set()
}

all_team_data = []

print("Processando arquivos...")
for csv_file in csv_files:
    year = os.path.basename(csv_file).split("_")[0]
    print(f"  {year}...", end=" ")
    
    # Ler apenas colunas essenciais
    try:
        df = pd.read_csv(csv_file, low_memory=False, usecols=lambda x: x in essential_cols)
    except:
        df = pd.read_csv(csv_file, low_memory=False)
        df = df[[c for c in essential_cols if c in df.columns]]
    
    stats['total_rows'] += len(df)
    
    # Separar dados de times
    df_teams = df[df['position'] == 'team'].copy()
    df_players = df[df['position'] != 'team'].copy()
    
    # Atualizar estatísticas
    n_games = df['gameid'].nunique()
    stats['games_by_year'][year] = n_games
    stats['total_games'] += n_games
    
    stats['leagues'].update(df['league'].dropna().unique())
    stats['teams'].update(df['teamname'].dropna().unique())
    stats['players'].update(df_players['playername'].dropna().unique())
    stats['champions'].update(df_players['champion'].dropna().unique())
    stats['patches'].update(df['patch'].dropna().astype(str).unique())
    stats['years'].update(df['year'].dropna().unique())
    
    # Coletar dados de times para análise
    all_team_data.append(df_teams)
    
    print(f"{n_games:,} partidas")
    
    del df, df_players
    gc.collect()

# Consolidar dados de times
print("\nConsolidando dados de times...")
df_teams_all = pd.concat(all_team_data, ignore_index=True)
del all_team_data
gc.collect()

print(f"\nTotal de registros de times: {len(df_teams_all):,}")

# Análise de variáveis-alvo
print("\n" + "=" * 80)
print("ANÁLISE DE VARIÁVEIS-ALVO")
print("=" * 80)

target_vars = ['result', 'gamelength', 'dragons', 'barons', 'towers', 
               'firstblood', 'firstdragon', 'firstbaron', 'firsttower']

target_stats = {}
for var in target_vars:
    if var in df_teams_all.columns:
        col = df_teams_all[var]
        target_stats[var] = {
            'unique': int(col.nunique()),
            'null_pct': float(col.isna().mean() * 100),
            'dtype': str(col.dtype)
        }
        if col.dtype in ['int64', 'float64']:
            target_stats[var]['min'] = float(col.min()) if pd.notna(col.min()) else None
            target_stats[var]['max'] = float(col.max()) if pd.notna(col.max()) else None
            target_stats[var]['mean'] = float(col.mean()) if pd.notna(col.mean()) else None
        print(f"\n{var}:")
        print(f"  Únicos: {target_stats[var]['unique']}, Nulos: {target_stats[var]['null_pct']:.1f}%")
        if 'mean' in target_stats[var]:
            print(f"  Min: {target_stats[var]['min']}, Max: {target_stats[var]['max']}, Média: {target_stats[var]['mean']:.2f}")

# Análise de draft (bans)
print("\n" + "=" * 80)
print("ANÁLISE DE DRAFT (BANS)")
print("=" * 80)

ban_cols = ['ban1', 'ban2', 'ban3', 'ban4', 'ban5']
available_bans = [c for c in ban_cols if c in df_teams_all.columns]
print(f"Colunas de ban disponíveis: {available_bans}")

if available_bans:
    ban_completeness = {}
    for col in available_bans:
        pct = (1 - df_teams_all[col].isna().mean()) * 100
        ban_completeness[col] = pct
        print(f"  {col}: {pct:.1f}% preenchido")

# Análise por liga
print("\n" + "=" * 80)
print("TOP 30 LIGAS POR NÚMERO DE PARTIDAS")
print("=" * 80)

league_games = df_teams_all.groupby('league')['gameid'].nunique().sort_values(ascending=False)
top_leagues = league_games.head(30)
print(top_leagues.to_string())

# Análise de completude por ano
print("\n" + "=" * 80)
print("COMPLETUDE DE DADOS POR ANO")
print("=" * 80)

completeness_data = []
for year in sorted(df_teams_all['year'].dropna().unique()):
    year_data = df_teams_all[df_teams_all['year'] == year]
    row = {
        'ano': int(year),
        'partidas': year_data['gameid'].nunique()
    }
    for col in ['result', 'gamelength', 'dragons', 'barons', 'firstblood', 'patch']:
        if col in year_data.columns:
            row[f'{col}_pct'] = round((1 - year_data[col].isna().mean()) * 100, 1)
    completeness_data.append(row)

completeness_df = pd.DataFrame(completeness_data)
print(completeness_df.to_string(index=False))

# Converter sets para listas para JSON
stats['leagues'] = sorted(list(stats['leagues']))
stats['teams'] = list(stats['teams'])
stats['players'] = list(stats['players'])
stats['champions'] = sorted(list(stats['champions']))
stats['patches'] = sorted(list(stats['patches']))
stats['years'] = sorted([int(y) for y in stats['years']])
stats['target_variables'] = target_stats
stats['top_leagues'] = top_leagues.to_dict()
stats['completeness_by_year'] = completeness_data

# Salvar estatísticas
with open(os.path.join(output_dir, "dataset_stats.json"), "w") as f:
    json.dump(stats, f, indent=2, default=str)

# Salvar resumo
summary = {
    'total_linhas': stats['total_rows'],
    'total_partidas': stats['total_games'],
    'total_ligas': len(stats['leagues']),
    'total_times': len(stats['teams']),
    'total_jogadores': len(stats['players']),
    'total_campeoes': len(stats['champions']),
    'total_patches': len(stats['patches']),
    'periodo': f"{min(stats['years'])} - {max(stats['years'])}"
}

print("\n" + "=" * 80)
print("RESUMO FINAL")
print("=" * 80)
for k, v in summary.items():
    print(f"  {k}: {v:,}" if isinstance(v, int) else f"  {k}: {v}")

with open(os.path.join(output_dir, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("\nArquivos salvos:")
print("  - dataset_stats.json")
print("  - summary.json")
print("\nAnálise concluída!")
