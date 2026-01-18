#!/usr/bin/env python3
"""
Script completo para criar:
1. Parquet por ano (dados brutos completos)
2. Parquet geral consolidado
3. JSON por ano (estatísticas e insights)
4. Markdown por ano (relatório legível)
"""

import pandas as pd
import numpy as np
import json
import os
import glob
import gc

# Diretórios
upload_dir = "/home/ubuntu/upload/"
data_dir = "/home/ubuntu/lol_prediction_project/data/"
by_year_dir = os.path.join(data_dir, "by_year/")
parquet_dir = os.path.join(data_dir, "parquet/")

os.makedirs(by_year_dir, exist_ok=True)
os.makedirs(parquet_dir, exist_ok=True)

print("=" * 80)
print("CRIAÇÃO DE ARQUIVOS DE DADOS LOL ESPORTS")
print("=" * 80)

# ============================================================================
# PARTE 1: CRIAR PARQUET POR ANO E PARQUET GERAL
# ============================================================================
print("\n" + "=" * 80)
print("PARTE 1: CRIANDO ARQUIVOS PARQUET")
print("=" * 80)

csv_files = sorted(glob.glob(os.path.join(upload_dir, "*_LoL_esports_match_data_from_OraclesElixir.csv")))

all_dfs = []

for csv_file in csv_files:
    year = os.path.basename(csv_file).split("_")[0]
    print(f"\nProcessando {year}...")
    
    # Ler CSV
    df = pd.read_csv(csv_file, low_memory=False)
    df['source_file'] = year
    
    print(f"  Linhas: {len(df):,}")
    
    # Salvar Parquet individual do ano
    parquet_path = os.path.join(parquet_dir, f"lol_esports_{year}.parquet")
    df.to_parquet(parquet_path, index=False)
    print(f"  -> {parquet_path}")
    
    all_dfs.append(df)
    gc.collect()

# Criar Parquet geral consolidado
print("\nCriando Parquet geral consolidado...")
df_all = pd.concat(all_dfs, ignore_index=True)
print(f"Total de linhas: {len(df_all):,}")

general_parquet = os.path.join(parquet_dir, "lol_esports_ALL_YEARS.parquet")
df_all.to_parquet(general_parquet, index=False)
print(f"  -> {general_parquet}")

# Liberar memória
del all_dfs
gc.collect()

# ============================================================================
# PARTE 2: CRIAR JSON E MARKDOWN POR ANO
# ============================================================================
print("\n" + "=" * 80)
print("PARTE 2: CRIANDO ARQUIVOS JSON E MARKDOWN POR ANO")
print("=" * 80)

def convert_to_serializable(obj):
    """Converte objetos numpy para tipos Python nativos"""
    if isinstance(obj, dict):
        return {str(k): convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return round(float(obj), 2) if not np.isnan(obj) else None
    elif isinstance(obj, np.ndarray):
        return [convert_to_serializable(x) for x in obj.tolist()]
    elif isinstance(obj, list):
        return [convert_to_serializable(x) for x in obj]
    elif pd.isna(obj):
        return None
    else:
        return obj

# Separar dados de times e jogadores
df_teams = df_all[df_all['position'] == 'team'].copy()
df_players = df_all[df_all['position'] != 'team'].copy()

# Criar dataset de matches
print("\nCriando dataset de matches...")
blue = df_teams[df_teams['side'] == 'Blue'].copy()
red = df_teams[df_teams['side'] == 'Red'].copy()

merge_keys = ['gameid', 'league', 'year', 'split', 'patch', 'date', 'gamelength']
blue_rename = {c: f'blue_{c}' for c in blue.columns if c not in merge_keys}
red_rename = {c: f'red_{c}' for c in red.columns if c not in merge_keys}

blue = blue.rename(columns=blue_rename)
red = red.rename(columns=red_rename)

df_matches = blue.merge(red, on=merge_keys, how='inner')
df_matches['winner'] = df_matches['blue_result'].apply(lambda x: 'Blue' if x == 1 else 'Red')

del blue, red
gc.collect()

# Processar cada ano
years = sorted(df_all['year'].dropna().unique())

for year in years:
    year = int(year)
    print(f"\n--- Processando {year} (JSON/MD) ---")
    
    # Filtrar dados do ano
    teams_year = df_teams[df_teams['year'] == year].copy()
    players_year = df_players[df_players['year'] == year].copy()
    matches_year = df_matches[df_matches['year'] == year].copy()
    
    n_games = len(matches_year)
    if n_games == 0:
        print(f"  Sem partidas para {year}, pulando...")
        continue
    
    # ========== CRIAR JSON ==========
    data = {
        'ano': year,
        'resumo': {
            'total_partidas': n_games,
            'total_times': int(teams_year['teamname'].nunique()),
            'total_jogadores': int(players_year['playername'].nunique()),
            'total_campeoes': int(players_year['champion'].nunique()),
            'total_ligas': int(teams_year['league'].nunique()),
            'total_patches': int(teams_year['patch'].nunique()),
            'duracao_media_min': round(matches_year['gamelength'].mean() / 60, 1),
            'blue_winrate': round((matches_year['winner'] == 'Blue').mean() * 100, 1)
        },
        'patches': {},
        'ligas': {},
        'times': {},
        'jogadores': {},
        'campeoes': {},
        'bans_mais_comuns': {}
    }
    
    # Dados por patch
    for patch in teams_year['patch'].dropna().unique():
        patch_data = teams_year[teams_year['patch'] == patch]
        patch_matches = matches_year[matches_year['patch'] == patch]
        patch_players = players_year[players_year['patch'] == patch]
        
        n_patch = len(patch_matches)
        if n_patch == 0:
            continue
        
        # Top campeões do patch
        champ_stats = patch_players.groupby('champion').agg({
            'gameid': 'count',
            'result': 'mean'
        }).rename(columns={'gameid': 'games', 'result': 'winrate'})
        champ_stats['winrate'] = (champ_stats['winrate'] * 100).round(1)
        top_champs = champ_stats.nlargest(15, 'games').to_dict('index')
        
        data['patches'][str(patch)] = {
            'partidas': n_patch,
            'duracao_media_min': round(patch_matches['gamelength'].mean() / 60, 1),
            'blue_winrate': round((patch_matches['winner'] == 'Blue').mean() * 100, 1),
            'campeoes_unicos': int(patch_players['champion'].nunique()),
            'top_campeoes': top_champs
        }
    
    # Dados por liga
    for league in teams_year['league'].unique():
        league_teams = teams_year[teams_year['league'] == league]
        league_matches = matches_year[matches_year['league'] == league]
        league_players = players_year[players_year['league'] == league]
        
        n_league = len(league_matches)
        if n_league == 0:
            continue
        
        # Top times
        team_stats = league_teams.groupby('teamname').agg({
            'gameid': 'count',
            'result': 'mean'
        }).rename(columns={'gameid': 'games', 'result': 'winrate'})
        team_stats['winrate'] = (team_stats['winrate'] * 100).round(1)
        top_teams = team_stats.nlargest(10, 'games').to_dict('index')
        
        # Top campeões
        champ_stats = league_players.groupby('champion').agg({
            'gameid': 'count',
            'result': 'mean'
        }).rename(columns={'gameid': 'games', 'result': 'winrate'})
        champ_stats['winrate'] = (champ_stats['winrate'] * 100).round(1)
        top_champs = champ_stats.nlargest(10, 'games').to_dict('index')
        
        data['ligas'][league] = {
            'partidas': n_league,
            'times_unicos': int(league_teams['teamname'].nunique()),
            'jogadores_unicos': int(league_players['playername'].nunique()),
            'duracao_media_min': round(league_matches['gamelength'].mean() / 60, 1),
            'blue_winrate': round((league_matches['winner'] == 'Blue').mean() * 100, 1),
            'top_times': top_teams,
            'top_campeoes': top_champs
        }
    
    # Dados por time (mínimo 5 jogos)
    for team in teams_year['teamname'].unique():
        team_data = teams_year[teams_year['teamname'] == team]
        n_team = team_data['gameid'].nunique()
        
        if n_team < 5:
            continue
        
        data['times'][team] = {
            'partidas': n_team,
            'winrate': round(team_data['result'].mean() * 100, 1),
            'kills_media': round(team_data['kills'].mean(), 1),
            'deaths_media': round(team_data['deaths'].mean(), 1),
            'dragons_media': round(team_data['dragons'].mean(), 2) if 'dragons' in team_data.columns else None,
            'barons_media': round(team_data['barons'].mean(), 2) if 'barons' in team_data.columns else None,
            'patches': list(team_data['patch'].dropna().unique())[:10],
            'ligas': list(team_data['league'].unique())
        }
    
    # Dados por jogador (mínimo 10 jogos)
    for player in players_year['playername'].dropna().unique():
        player_data = players_year[players_year['playername'] == player]
        n_player = player_data['gameid'].nunique()
        
        if n_player < 10:
            continue
        
        champ_counts = player_data['champion'].value_counts().head(5).to_dict()
        main_pos = player_data['position'].mode().iloc[0] if len(player_data) > 0 else 'unknown'
        
        data['jogadores'][player] = {
            'partidas': n_player,
            'winrate': round(player_data['result'].mean() * 100, 1),
            'kda_kills': round(player_data['kills'].mean(), 1),
            'kda_deaths': round(player_data['deaths'].mean(), 1),
            'kda_assists': round(player_data['assists'].mean(), 1),
            'posicao': main_pos,
            'campeoes_mais_jogados': champ_counts,
            'times': list(player_data['teamname'].unique())
        }
    
    # Dados por campeão (mínimo 5 jogos)
    for champ in players_year['champion'].dropna().unique():
        champ_data = players_year[players_year['champion'] == champ]
        n_champ = len(champ_data)
        
        if n_champ < 5:
            continue
        
        positions = champ_data['position'].value_counts().to_dict()
        
        # Win rate por patch
        wr_patch = champ_data.groupby('patch')['result'].agg(['count', 'mean'])
        wr_patch['mean'] = (wr_patch['mean'] * 100).round(1)
        wr_patch = wr_patch[wr_patch['count'] >= 3].to_dict('index')
        
        data['campeoes'][champ] = {
            'partidas': n_champ,
            'winrate': round(champ_data['result'].mean() * 100, 1),
            'posicoes': positions,
            'winrate_por_patch': wr_patch
        }
    
    # Bans mais comuns
    ban_cols = ['ban1', 'ban2', 'ban3', 'ban4', 'ban5']
    all_bans = []
    for col in ban_cols:
        if col in teams_year.columns:
            all_bans.extend(teams_year[col].dropna().tolist())
    
    if all_bans:
        ban_counts = pd.Series(all_bans).value_counts().head(20).to_dict()
        data['bans_mais_comuns'] = ban_counts
    
    # Salvar JSON
    json_data = convert_to_serializable(data)
    json_path = os.path.join(by_year_dir, f"lol_esports_{year}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"  -> {json_path}")
    
    # ========== CRIAR MARKDOWN ==========
    md = f"""# Dados de LoL Esports - {year}

## Resumo Geral

| Métrica | Valor |
|---------|-------|
| Total de Partidas | {data['resumo']['total_partidas']:,} |
| Total de Times | {data['resumo']['total_times']:,} |
| Total de Jogadores | {data['resumo']['total_jogadores']:,} |
| Total de Campeões | {data['resumo']['total_campeoes']} |
| Total de Ligas | {data['resumo']['total_ligas']} |
| Total de Patches | {data['resumo']['total_patches']} |
| Duração Média (min) | {data['resumo']['duracao_media_min']} |
| Blue Side Win Rate | {data['resumo']['blue_winrate']}% |

---

## Dados por Patch

"""
    
    # Patches ordenados
    sorted_patches = sorted(data['patches'].items(), key=lambda x: str(x[0]))
    for patch, pdata in sorted_patches:
        md += f"""### Patch {patch}

| Métrica | Valor |
|---------|-------|
| Partidas | {pdata['partidas']} |
| Duração Média | {pdata['duracao_media_min']} min |
| Blue Win Rate | {pdata['blue_winrate']}% |
| Campeões Únicos | {pdata['campeoes_unicos']} |

**Top Campeões:**

| Campeão | Partidas | Win Rate |
|---------|----------|----------|
"""
        for champ, stats in list(pdata['top_campeoes'].items())[:10]:
            md += f"| {champ} | {stats['games']} | {stats['winrate']}% |\n"
        md += "\n"
    
    # Ligas
    md += "---\n\n## Dados por Liga/Região\n\n"
    sorted_leagues = sorted(data['ligas'].items(), key=lambda x: x[1]['partidas'], reverse=True)
    
    for league, ldata in sorted_leagues[:15]:
        md += f"""### {league}

| Métrica | Valor |
|---------|-------|
| Partidas | {ldata['partidas']} |
| Times Únicos | {ldata['times_unicos']} |
| Jogadores Únicos | {ldata['jogadores_unicos']} |
| Duração Média | {ldata['duracao_media_min']} min |
| Blue Win Rate | {ldata['blue_winrate']}% |

**Top Times:**

| Time | Partidas | Win Rate |
|------|----------|----------|
"""
        for team, stats in list(ldata['top_times'].items())[:5]:
            md += f"| {team} | {stats['games']} | {stats['winrate']}% |\n"
        md += "\n"
    
    # Top Times
    md += "---\n\n## Top Times do Ano\n\n"
    md += "| Time | Partidas | Win Rate | Ligas |\n"
    md += "|------|----------|----------|-------|\n"
    
    sorted_teams = sorted(data['times'].items(), key=lambda x: x[1]['partidas'], reverse=True)
    for team, stats in sorted_teams[:30]:
        ligas = ', '.join(stats['ligas'][:3])
        md += f"| {team} | {stats['partidas']} | {stats['winrate']}% | {ligas} |\n"
    
    # Top Jogadores
    md += "\n---\n\n## Top Jogadores do Ano\n\n"
    md += "| Jogador | Partidas | Win Rate | Posição | KDA |\n"
    md += "|---------|----------|----------|---------|-----|\n"
    
    sorted_players = sorted(data['jogadores'].items(), key=lambda x: x[1]['partidas'], reverse=True)
    for player, stats in sorted_players[:50]:
        kda = f"{stats['kda_kills']}/{stats['kda_deaths']}/{stats['kda_assists']}"
        md += f"| {player} | {stats['partidas']} | {stats['winrate']}% | {stats['posicao']} | {kda} |\n"
    
    # Top Campeões
    md += "\n---\n\n## Top Campeões do Ano\n\n"
    md += "| Campeão | Partidas | Win Rate |\n"
    md += "|---------|----------|----------|\n"
    
    sorted_champs = sorted(data['campeoes'].items(), key=lambda x: x[1]['partidas'], reverse=True)
    for champ, stats in sorted_champs[:30]:
        md += f"| {champ} | {stats['partidas']} | {stats['winrate']}% |\n"
    
    # Bans
    if data['bans_mais_comuns']:
        md += "\n---\n\n## Campeões Mais Banidos\n\n"
        md += "| Campeão | Total de Bans |\n"
        md += "|---------|---------------|\n"
        for champ, count in list(data['bans_mais_comuns'].items())[:15]:
            md += f"| {champ} | {count} |\n"
    
    # Salvar Markdown
    md_path = os.path.join(by_year_dir, f"lol_esports_{year}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"  -> {md_path}")
    
    gc.collect()

# ============================================================================
# RESUMO FINAL
# ============================================================================
print("\n" + "=" * 80)
print("CRIAÇÃO DE ARQUIVOS CONCLUÍDA")
print("=" * 80)

print("\nArquivos Parquet:")
for f in sorted(os.listdir(parquet_dir)):
    path = os.path.join(parquet_dir, f)
    size = os.path.getsize(path) / (1024*1024)
    print(f"  {f}: {size:.1f} MB")

print("\nArquivos por ano (JSON/MD):")
for f in sorted(os.listdir(by_year_dir)):
    path = os.path.join(by_year_dir, f)
    size = os.path.getsize(path) / 1024
    print(f"  {f}: {size:.1f} KB")
