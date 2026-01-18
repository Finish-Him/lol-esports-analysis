#!/usr/bin/env python3
"""
Script para completar os arquivos JSON e MD faltantes (2024, 2025, 2026)
"""

import pandas as pd
import numpy as np
import json
import os
import gc

# Diretórios
parquet_dir = "/home/ubuntu/lol_prediction_project/data/parquet/"
by_year_dir = "/home/ubuntu/lol_prediction_project/data/by_year/"

def convert_to_serializable(obj):
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

# Anos faltantes
missing_years = [2024, 2025, 2026]

for year in missing_years:
    print(f"\n--- Processando {year} ---")
    
    # Carregar parquet do ano
    parquet_path = os.path.join(parquet_dir, f"lol_esports_{year}.parquet")
    df = pd.read_parquet(parquet_path)
    
    df_teams = df[df['position'] == 'team'].copy()
    df_players = df[df['position'] != 'team'].copy()
    
    # Criar matches
    blue = df_teams[df_teams['side'] == 'Blue'].copy()
    red = df_teams[df_teams['side'] == 'Red'].copy()
    
    merge_keys = ['gameid', 'league', 'year', 'split', 'patch', 'date', 'gamelength']
    blue_rename = {c: f'blue_{c}' for c in blue.columns if c not in merge_keys}
    red_rename = {c: f'red_{c}' for c in red.columns if c not in merge_keys}
    
    blue = blue.rename(columns=blue_rename)
    red = red.rename(columns=red_rename)
    
    matches = blue.merge(red, on=merge_keys, how='inner')
    matches['winner'] = matches['blue_result'].apply(lambda x: 'Blue' if x == 1 else 'Red')
    
    n_games = len(matches)
    
    # Criar JSON
    data = {
        'ano': year,
        'resumo': {
            'total_partidas': n_games,
            'total_times': int(df_teams['teamname'].nunique()),
            'total_jogadores': int(df_players['playername'].nunique()),
            'total_campeoes': int(df_players['champion'].nunique()),
            'total_ligas': int(df_teams['league'].nunique()),
            'total_patches': int(df_teams['patch'].nunique()),
            'duracao_media_min': round(matches['gamelength'].mean() / 60, 1) if n_games > 0 else 0,
            'blue_winrate': round((matches['winner'] == 'Blue').mean() * 100, 1) if n_games > 0 else 50
        },
        'patches': {},
        'ligas': {},
        'times': {},
        'jogadores': {},
        'campeoes': {},
        'bans_mais_comuns': {}
    }
    
    # Patches
    for patch in df_teams['patch'].dropna().unique():
        patch_teams = df_teams[df_teams['patch'] == patch]
        patch_matches = matches[matches['patch'] == patch]
        patch_players = df_players[df_players['patch'] == patch]
        
        n_patch = len(patch_matches)
        if n_patch == 0:
            continue
        
        champ_stats = patch_players.groupby('champion').agg({
            'gameid': 'count', 'result': 'mean'
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
    
    # Ligas
    for league in df_teams['league'].unique():
        league_teams = df_teams[df_teams['league'] == league]
        league_matches = matches[matches['league'] == league]
        league_players = df_players[df_players['league'] == league]
        
        n_league = len(league_matches)
        if n_league == 0:
            continue
        
        team_stats = league_teams.groupby('teamname').agg({
            'gameid': 'count', 'result': 'mean'
        }).rename(columns={'gameid': 'games', 'result': 'winrate'})
        team_stats['winrate'] = (team_stats['winrate'] * 100).round(1)
        top_teams = team_stats.nlargest(10, 'games').to_dict('index')
        
        champ_stats = league_players.groupby('champion').agg({
            'gameid': 'count', 'result': 'mean'
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
    
    # Times
    for team in df_teams['teamname'].unique():
        team_data = df_teams[df_teams['teamname'] == team]
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
    
    # Jogadores
    for player in df_players['playername'].dropna().unique():
        player_data = df_players[df_players['playername'] == player]
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
    
    # Campeões
    for champ in df_players['champion'].dropna().unique():
        champ_data = df_players[df_players['champion'] == champ]
        n_champ = len(champ_data)
        if n_champ < 5:
            continue
        
        positions = champ_data['position'].value_counts().to_dict()
        wr_patch = champ_data.groupby('patch')['result'].agg(['count', 'mean'])
        wr_patch['mean'] = (wr_patch['mean'] * 100).round(1)
        wr_patch = wr_patch[wr_patch['count'] >= 3].to_dict('index')
        
        data['campeoes'][champ] = {
            'partidas': n_champ,
            'winrate': round(champ_data['result'].mean() * 100, 1),
            'posicoes': positions,
            'winrate_por_patch': wr_patch
        }
    
    # Bans
    ban_cols = ['ban1', 'ban2', 'ban3', 'ban4', 'ban5']
    all_bans = []
    for col in ban_cols:
        if col in df_teams.columns:
            all_bans.extend(df_teams[col].dropna().tolist())
    if all_bans:
        data['bans_mais_comuns'] = pd.Series(all_bans).value_counts().head(20).to_dict()
    
    # Salvar JSON
    json_data = convert_to_serializable(data)
    json_path = os.path.join(by_year_dir, f"lol_esports_{year}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"  -> {json_path}")
    
    # Criar Markdown
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
    
    for patch, pdata in sorted(data['patches'].items(), key=lambda x: str(x[0])):
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
    
    md += "---\n\n## Dados por Liga/Região\n\n"
    for league, ldata in sorted(data['ligas'].items(), key=lambda x: x[1]['partidas'], reverse=True)[:15]:
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
    
    md += "---\n\n## Top Times do Ano\n\n"
    md += "| Time | Partidas | Win Rate | Ligas |\n"
    md += "|------|----------|----------|-------|\n"
    for team, stats in sorted(data['times'].items(), key=lambda x: x[1]['partidas'], reverse=True)[:30]:
        ligas = ', '.join(stats['ligas'][:3])
        md += f"| {team} | {stats['partidas']} | {stats['winrate']}% | {ligas} |\n"
    
    md += "\n---\n\n## Top Jogadores do Ano\n\n"
    md += "| Jogador | Partidas | Win Rate | Posição | KDA |\n"
    md += "|---------|----------|----------|---------|-----|\n"
    for player, stats in sorted(data['jogadores'].items(), key=lambda x: x[1]['partidas'], reverse=True)[:50]:
        kda = f"{stats['kda_kills']}/{stats['kda_deaths']}/{stats['kda_assists']}"
        md += f"| {player} | {stats['partidas']} | {stats['winrate']}% | {stats['posicao']} | {kda} |\n"
    
    md += "\n---\n\n## Top Campeões do Ano\n\n"
    md += "| Campeão | Partidas | Win Rate |\n"
    md += "|---------|----------|----------|\n"
    for champ, stats in sorted(data['campeoes'].items(), key=lambda x: x[1]['partidas'], reverse=True)[:30]:
        md += f"| {champ} | {stats['partidas']} | {stats['winrate']}% |\n"
    
    if data['bans_mais_comuns']:
        md += "\n---\n\n## Campeões Mais Banidos\n\n"
        md += "| Campeão | Total de Bans |\n"
        md += "|---------|---------------|\n"
        for champ, count in list(data['bans_mais_comuns'].items())[:15]:
            md += f"| {champ} | {count} |\n"
    
    md_path = os.path.join(by_year_dir, f"lol_esports_{year}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"  -> {md_path}")
    
    del df, df_teams, df_players, matches
    gc.collect()

print("\nArquivos faltantes criados com sucesso!")
