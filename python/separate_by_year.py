#!/usr/bin/env python3
"""
Script para separar dados de LoL Esports por ano em arquivos Markdown e JSON
Cada ano terá seu próprio arquivo com estatísticas detalhadas por patch, região e jogador
"""

import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict

# Diretórios
data_dir = "/home/ubuntu/lol_prediction_project/data/"
output_dir = "/home/ubuntu/lol_prediction_project/data/by_year/"
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("SEPARAÇÃO DE DADOS POR ANO")
print("=" * 80)

# Carregar dados consolidados
print("\nCarregando dados...")
df_teams = pd.read_parquet(os.path.join(data_dir, "lol_esports_teams.parquet"))
df_players = pd.read_parquet(os.path.join(data_dir, "lol_esports_players.parquet"))
df_matches = pd.read_parquet(os.path.join(data_dir, "lol_esports_matches.parquet"))
df_draft = pd.read_parquet(os.path.join(data_dir, "lol_esports_draft.parquet"))

print(f"  Times: {len(df_teams):,}")
print(f"  Jogadores: {len(df_players):,}")
print(f"  Partidas: {len(df_matches):,}")

# Obter anos únicos
years = sorted(df_teams['year'].dropna().unique())
print(f"\nAnos disponíveis: {[int(y) for y in years]}")

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

def generate_year_data(year):
    """Gera dados completos para um ano específico"""
    year = int(year)
    print(f"\n--- Processando {year} ---")
    
    # Filtrar dados do ano
    teams_year = df_teams[df_teams['year'] == year].copy()
    players_year = df_players[df_players['year'] == year].copy()
    matches_year = df_matches[df_matches['year'] == year].copy()
    draft_year = df_draft[df_draft['year'] == year].copy()
    
    data = {
        'ano': year,
        'resumo': {},
        'patches': {},
        'ligas': {},
        'times': {},
        'jogadores': {},
        'campeoes': {},
        'draft': {}
    }
    
    # ========== RESUMO GERAL ==========
    n_games = len(matches_year)
    data['resumo'] = {
        'total_partidas': n_games,
        'total_times': teams_year['teamname'].nunique(),
        'total_jogadores': players_year['playername'].nunique(),
        'total_campeoes': players_year['champion'].nunique(),
        'total_ligas': teams_year['league'].nunique(),
        'total_patches': teams_year['patch'].nunique(),
        'duracao_media_min': round(matches_year['gamelength'].mean() / 60, 1) if n_games > 0 else 0,
        'blue_winrate': round((matches_year['winner'] == 'Blue').mean() * 100, 1) if n_games > 0 else 50
    }
    
    # ========== DADOS POR PATCH ==========
    patches = teams_year['patch'].dropna().unique()
    for patch in sorted(patches, key=lambda x: str(x)):
        patch_teams = teams_year[teams_year['patch'] == patch]
        patch_matches = matches_year[matches_year['patch'] == patch]
        patch_players = players_year[players_year['patch'] == patch]
        
        n_patch_games = len(patch_matches)
        if n_patch_games == 0:
            continue
            
        # Top campeões do patch
        champ_stats = patch_players.groupby('champion').agg({
            'gameid': 'count',
            'result': 'mean'
        }).rename(columns={'gameid': 'games', 'result': 'winrate'})
        champ_stats['winrate'] = (champ_stats['winrate'] * 100).round(1)
        top_champs = champ_stats.nlargest(10, 'games').to_dict('index')
        
        data['patches'][str(patch)] = {
            'partidas': n_patch_games,
            'duracao_media_min': round(patch_matches['gamelength'].mean() / 60, 1),
            'blue_winrate': round((patch_matches['winner'] == 'Blue').mean() * 100, 1),
            'campeoes_unicos': patch_players['champion'].nunique(),
            'top_campeoes': top_champs
        }
    
    # ========== DADOS POR LIGA/REGIÃO ==========
    leagues = teams_year['league'].unique()
    for league in sorted(leagues):
        league_teams = teams_year[teams_year['league'] == league]
        league_matches = matches_year[matches_year['league'] == league]
        league_players = players_year[players_year['league'] == league]
        
        n_league_games = len(league_matches)
        if n_league_games == 0:
            continue
        
        # Top times da liga
        team_stats = league_teams.groupby('teamname').agg({
            'gameid': 'count',
            'result': 'mean'
        }).rename(columns={'gameid': 'games', 'result': 'winrate'})
        team_stats['winrate'] = (team_stats['winrate'] * 100).round(1)
        top_teams = team_stats.nlargest(5, 'games').to_dict('index')
        
        # Top campeões da liga
        champ_stats = league_players.groupby('champion').agg({
            'gameid': 'count',
            'result': 'mean'
        }).rename(columns={'gameid': 'games', 'result': 'winrate'})
        champ_stats['winrate'] = (champ_stats['winrate'] * 100).round(1)
        top_champs = champ_stats.nlargest(10, 'games').to_dict('index')
        
        data['ligas'][league] = {
            'partidas': n_league_games,
            'times_unicos': league_teams['teamname'].nunique(),
            'jogadores_unicos': league_players['playername'].nunique(),
            'duracao_media_min': round(league_matches['gamelength'].mean() / 60, 1),
            'blue_winrate': round((league_matches['winner'] == 'Blue').mean() * 100, 1),
            'top_times': top_teams,
            'top_campeoes': top_champs
        }
    
    # ========== DADOS POR TIME ==========
    teams_list = teams_year['teamname'].unique()
    for team in teams_list:
        team_data = teams_year[teams_year['teamname'] == team]
        n_team_games = team_data['gameid'].nunique()
        
        if n_team_games < 5:  # Mínimo de 5 jogos
            continue
        
        # Patches jogados pelo time
        patches_played = team_data['patch'].dropna().unique().tolist()
        
        # Ligas participadas
        leagues_played = team_data['league'].unique().tolist()
        
        data['times'][team] = {
            'partidas': n_team_games,
            'winrate': round(team_data['result'].mean() * 100, 1),
            'kills_media': round(team_data['kills'].mean(), 1),
            'deaths_media': round(team_data['deaths'].mean(), 1),
            'dragons_media': round(team_data['dragons'].mean(), 2),
            'barons_media': round(team_data['barons'].mean(), 2),
            'torres_media': round(team_data['towers'].mean(), 2) if 'towers' in team_data.columns else None,
            'patches': patches_played[:10],  # Limitar para não ficar muito grande
            'ligas': leagues_played
        }
    
    # ========== DADOS POR JOGADOR ==========
    players_list = players_year['playername'].dropna().unique()
    for player in players_list:
        player_data = players_year[players_year['playername'] == player]
        n_player_games = player_data['gameid'].nunique()
        
        if n_player_games < 10:  # Mínimo de 10 jogos
            continue
        
        # Campeões mais jogados
        champ_counts = player_data['champion'].value_counts().head(5).to_dict()
        
        # Posição principal
        main_position = player_data['position'].mode().iloc[0] if len(player_data) > 0 else 'unknown'
        
        # Times jogados
        teams_played = player_data['teamname'].unique().tolist()
        
        data['jogadores'][player] = {
            'partidas': n_player_games,
            'winrate': round(player_data['result'].mean() * 100, 1),
            'kda_kills': round(player_data['kills'].mean(), 1),
            'kda_deaths': round(player_data['deaths'].mean(), 1),
            'kda_assists': round(player_data['assists'].mean(), 1),
            'posicao': main_position,
            'campeoes_mais_jogados': champ_counts,
            'times': teams_played
        }
    
    # ========== DADOS POR CAMPEÃO ==========
    champions = players_year['champion'].dropna().unique()
    for champ in champions:
        champ_data = players_year[players_year['champion'] == champ]
        n_champ_games = len(champ_data)
        
        if n_champ_games < 5:
            continue
        
        # Posições jogadas
        positions = champ_data['position'].value_counts().to_dict()
        
        # Win rate por patch
        wr_by_patch = champ_data.groupby('patch')['result'].agg(['count', 'mean'])
        wr_by_patch['mean'] = (wr_by_patch['mean'] * 100).round(1)
        wr_by_patch = wr_by_patch[wr_by_patch['count'] >= 3].to_dict('index')
        
        data['campeoes'][champ] = {
            'partidas': n_champ_games,
            'winrate': round(champ_data['result'].mean() * 100, 1),
            'posicoes': positions,
            'winrate_por_patch': wr_by_patch
        }
    
    # ========== DADOS DE DRAFT ==========
    # Bans mais comuns
    ban_cols = ['blue_ban1', 'blue_ban2', 'blue_ban3', 'blue_ban4', 'blue_ban5',
                'red_ban1', 'red_ban2', 'red_ban3', 'red_ban4', 'red_ban5']
    all_bans = []
    for col in ban_cols:
        if col in draft_year.columns:
            all_bans.extend(draft_year[col].dropna().tolist())
    
    if all_bans:
        ban_counts = pd.Series(all_bans).value_counts().head(20).to_dict()
        data['draft']['bans_mais_comuns'] = ban_counts
    
    return convert_to_serializable(data)

def generate_markdown(data):
    """Gera arquivo Markdown a partir dos dados do ano"""
    year = data['ano']
    resumo = data['resumo']
    
    md = f"""# Dados de LoL Esports - {year}

## Resumo Geral

| Métrica | Valor |
|---------|-------|
| Total de Partidas | {resumo['total_partidas']:,} |
| Total de Times | {resumo['total_times']:,} |
| Total de Jogadores | {resumo['total_jogadores']:,} |
| Total de Campeões Jogados | {resumo['total_campeoes']} |
| Total de Ligas | {resumo['total_ligas']} |
| Total de Patches | {resumo['total_patches']} |
| Duração Média (min) | {resumo['duracao_media_min']} |
| Blue Side Win Rate | {resumo['blue_winrate']}% |

---

## Dados por Patch

"""
    
    # Patches
    for patch, patch_data in sorted(data['patches'].items(), key=lambda x: str(x[0])):
        md += f"""### Patch {patch}

- **Partidas:** {patch_data['partidas']}
- **Duração Média:** {patch_data['duracao_media_min']} min
- **Blue Win Rate:** {patch_data['blue_winrate']}%
- **Campeões Únicos:** {patch_data['campeoes_unicos']}

**Top Campeões:**

| Campeão | Partidas | Win Rate |
|---------|----------|----------|
"""
        for champ, stats in list(patch_data['top_campeoes'].items())[:5]:
            md += f"| {champ} | {stats['games']} | {stats['winrate']}% |\n"
        md += "\n"
    
    # Ligas
    md += "---\n\n## Dados por Liga/Região\n\n"
    
    # Ordenar ligas por número de partidas
    sorted_leagues = sorted(data['ligas'].items(), key=lambda x: x[1]['partidas'], reverse=True)
    
    for league, league_data in sorted_leagues[:20]:  # Top 20 ligas
        md += f"""### {league}

- **Partidas:** {league_data['partidas']}
- **Times Únicos:** {league_data['times_unicos']}
- **Jogadores Únicos:** {league_data['jogadores_unicos']}
- **Duração Média:** {league_data['duracao_media_min']} min
- **Blue Win Rate:** {league_data['blue_winrate']}%

**Top Times:**

| Time | Partidas | Win Rate |
|------|----------|----------|
"""
        for team, stats in list(league_data['top_times'].items())[:5]:
            md += f"| {team} | {stats['games']} | {stats['winrate']}% |\n"
        md += "\n"
    
    # Top Times Geral
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
    md += "| Campeão | Partidas | Win Rate | Posições |\n"
    md += "|---------|----------|----------|----------|\n"
    
    sorted_champs = sorted(data['campeoes'].items(), key=lambda x: x[1]['partidas'], reverse=True)
    for champ, stats in sorted_champs[:30]:
        positions = ', '.join([f"{k}({v})" for k, v in list(stats['posicoes'].items())[:2]])
        md += f"| {champ} | {stats['partidas']} | {stats['winrate']}% | {positions} |\n"
    
    # Bans mais comuns
    if 'bans_mais_comuns' in data['draft']:
        md += "\n---\n\n## Campeões Mais Banidos\n\n"
        md += "| Campeão | Total de Bans |\n"
        md += "|---------|---------------|\n"
        for champ, count in list(data['draft']['bans_mais_comuns'].items())[:15]:
            md += f"| {champ} | {count} |\n"
    
    return md

# Processar cada ano
print("\nProcessando anos...")
for year in years:
    year = int(year)
    
    # Gerar dados
    year_data = generate_year_data(year)
    
    # Salvar JSON
    json_path = os.path.join(output_dir, f"lol_esports_{year}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(year_data, f, indent=2, ensure_ascii=False)
    print(f"  -> {json_path}")
    
    # Gerar e salvar Markdown
    md_content = generate_markdown(year_data)
    md_path = os.path.join(output_dir, f"lol_esports_{year}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"  -> {md_path}")

print("\n" + "=" * 80)
print("SEPARAÇÃO CONCLUÍDA")
print("=" * 80)

# Listar arquivos criados
print("\nArquivos criados:")
for f in sorted(os.listdir(output_dir)):
    path = os.path.join(output_dir, f)
    size = os.path.getsize(path)
    if size > 1024 * 1024:
        print(f"  {f}: {size / (1024*1024):.1f} MB")
    else:
        print(f"  {f}: {size / 1024:.1f} KB")
