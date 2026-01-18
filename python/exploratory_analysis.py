#!/usr/bin/env python3
"""
Análise Exploratória de Dados de LoL Esports
Gera insights sobre times, campeões, patches e tendências temporais
"""

import pandas as pd
import numpy as np
import json
import os

# Diretórios
data_dir = "/home/ubuntu/lol_prediction_project/data/"
output_dir = "/home/ubuntu/lol_prediction_project/analysis/"
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("ANÁLISE EXPLORATÓRIA DE DADOS DE LOL ESPORTS")
print("=" * 80)

# Carregar dados consolidados
print("\nCarregando dados...")
df_teams = pd.read_parquet(os.path.join(data_dir, "lol_esports_teams.parquet"))
df_matches = pd.read_parquet(os.path.join(data_dir, "lol_esports_matches.parquet"))
df_draft = pd.read_parquet(os.path.join(data_dir, "lol_esports_draft.parquet"))

print(f"  Times: {len(df_teams):,} registros")
print(f"  Partidas: {len(df_matches):,} registros")
print(f"  Draft: {len(df_draft):,} registros")

insights = {}

# ============================================================================
# 1. ANÁLISE TEMPORAL
# ============================================================================
print("\n" + "=" * 80)
print("1. ANÁLISE TEMPORAL")
print("=" * 80)

# Partidas por ano
games_by_year = df_matches.groupby('year').size()
print("\nPartidas por ano:")
print(games_by_year.to_string())

# Duração média por ano
avg_duration = df_matches.groupby('year')['gamelength'].mean() / 60  # em minutos
print("\nDuração média (minutos) por ano:")
print(avg_duration.round(1).to_string())

insights['temporal'] = {
    'games_by_year': games_by_year.to_dict(),
    'avg_duration_by_year': avg_duration.round(1).to_dict()
}

# ============================================================================
# 2. ANÁLISE DE LADO (BLUE VS RED)
# ============================================================================
print("\n" + "=" * 80)
print("2. ANÁLISE DE LADO (BLUE VS RED)")
print("=" * 80)

# Win rate por lado
blue_wins = (df_matches['winner'] == 'Blue').sum()
red_wins = (df_matches['winner'] == 'Red').sum()
total = len(df_matches)

print(f"\nWin rate geral:")
print(f"  Blue: {blue_wins:,} ({blue_wins/total*100:.1f}%)")
print(f"  Red: {red_wins:,} ({red_wins/total*100:.1f}%)")

# Win rate por lado por ano
side_wr_by_year = df_matches.groupby('year').apply(
    lambda x: (x['winner'] == 'Blue').mean() * 100
).round(1)
print("\nWin rate Blue por ano:")
print(side_wr_by_year.to_string())

insights['side_analysis'] = {
    'overall_blue_wr': round(blue_wins/total*100, 1),
    'overall_red_wr': round(red_wins/total*100, 1),
    'blue_wr_by_year': side_wr_by_year.to_dict()
}

# ============================================================================
# 3. ANÁLISE DE LIGAS
# ============================================================================
print("\n" + "=" * 80)
print("3. ANÁLISE DE LIGAS")
print("=" * 80)

# Top ligas por número de partidas
league_stats = df_matches.groupby('league').agg({
    'gameid': 'count',
    'gamelength': 'mean'
}).rename(columns={'gameid': 'games', 'gamelength': 'avg_duration'})
league_stats['avg_duration'] = (league_stats['avg_duration'] / 60).round(1)
league_stats = league_stats.sort_values('games', ascending=False)

print("\nTop 15 ligas:")
print(league_stats.head(15).to_string())

# Ligas principais (tier 1)
tier1_leagues = ['LCK', 'LPL', 'LEC', 'LCS', 'NA LCS', 'EU LCS', 'WLDs', 'MSI']
tier1_data = df_matches[df_matches['league'].isin(tier1_leagues)]
print(f"\nPartidas em ligas Tier 1: {len(tier1_data):,} ({len(tier1_data)/len(df_matches)*100:.1f}%)")

insights['leagues'] = {
    'top_leagues': league_stats.head(20).to_dict(),
    'tier1_games': len(tier1_data),
    'tier1_percentage': round(len(tier1_data)/len(df_matches)*100, 1)
}

# ============================================================================
# 4. ANÁLISE DE OBJETIVOS
# ============================================================================
print("\n" + "=" * 80)
print("4. ANÁLISE DE OBJETIVOS")
print("=" * 80)

# Correlação entre first objectives e vitória
first_objectives = ['blue_firstblood', 'blue_firstdragon', 'blue_firstbaron', 
                    'blue_firsttower', 'blue_firstherald']

print("\nImpacto de First Objectives na vitória (Blue side):")
for obj in first_objectives:
    if obj in df_matches.columns:
        # Filtrar apenas partidas com dados
        valid = df_matches[df_matches[obj].notna()]
        if len(valid) > 0:
            wr_with = (valid[valid[obj] == 1]['blue_result'] == 1).mean() * 100
            wr_without = (valid[valid[obj] == 0]['blue_result'] == 1).mean() * 100
            obj_name = obj.replace('blue_', '')
            print(f"  {obj_name}: Com={wr_with:.1f}%, Sem={wr_without:.1f}%, Delta={wr_with-wr_without:.1f}%")

# Média de objetivos por partida
print("\nMédia de objetivos por partida (time vencedor vs perdedor):")
winner_stats = df_matches[df_matches['blue_result'] == 1][['blue_dragons', 'blue_barons', 'blue_towers']].mean()
loser_stats = df_matches[df_matches['blue_result'] == 0][['blue_dragons', 'blue_barons', 'blue_towers']].mean()
print(f"  Dragons - Vencedor: {winner_stats['blue_dragons']:.2f}, Perdedor: {loser_stats['blue_dragons']:.2f}")
print(f"  Barons - Vencedor: {winner_stats['blue_barons']:.2f}, Perdedor: {loser_stats['blue_barons']:.2f}")
print(f"  Towers - Vencedor: {winner_stats['blue_towers']:.2f}, Perdedor: {loser_stats['blue_towers']:.2f}")

insights['objectives'] = {
    'winner_avg_dragons': round(winner_stats['blue_dragons'], 2),
    'winner_avg_barons': round(winner_stats['blue_barons'], 2),
    'winner_avg_towers': round(winner_stats['blue_towers'], 2),
    'loser_avg_dragons': round(loser_stats['blue_dragons'], 2),
    'loser_avg_barons': round(loser_stats['blue_barons'], 2),
    'loser_avg_towers': round(loser_stats['blue_towers'], 2)
}

# ============================================================================
# 5. ANÁLISE DE TIMES
# ============================================================================
print("\n" + "=" * 80)
print("5. ANÁLISE DE TIMES")
print("=" * 80)

# Win rate por time (mínimo 50 partidas)
team_stats = df_teams.groupby('teamname').agg({
    'gameid': 'count',
    'result': 'mean'
}).rename(columns={'gameid': 'games', 'result': 'winrate'})
team_stats['winrate'] = (team_stats['winrate'] * 100).round(1)
team_stats = team_stats[team_stats['games'] >= 50].sort_values('winrate', ascending=False)

print("\nTop 20 times por win rate (min 50 partidas):")
print(team_stats.head(20).to_string())

# Times mais ativos
most_active = team_stats.sort_values('games', ascending=False).head(20)
print("\nTop 20 times mais ativos:")
print(most_active.to_string())

insights['teams'] = {
    'top_winrate': team_stats.head(20).to_dict(),
    'most_active': most_active.to_dict()
}

# ============================================================================
# 6. ANÁLISE DE PATCHES
# ============================================================================
print("\n" + "=" * 80)
print("6. ANÁLISE DE PATCHES")
print("=" * 80)

# Partidas por patch
patch_stats = df_matches.groupby('patch').agg({
    'gameid': 'count',
    'gamelength': 'mean'
}).rename(columns={'gameid': 'games', 'gamelength': 'avg_duration'})
patch_stats['avg_duration'] = (patch_stats['avg_duration'] / 60).round(1)
patch_stats = patch_stats.sort_values('games', ascending=False)

print("\nTop 20 patches por número de partidas:")
print(patch_stats.head(20).to_string())

# Patches recentes (2024-2026)
recent_patches = df_matches[df_matches['year'] >= 2024]['patch'].unique()
print(f"\nPatches em 2024-2026: {len(recent_patches)}")

insights['patches'] = {
    'top_patches': patch_stats.head(30).to_dict(),
    'recent_patches': list(recent_patches)
}

# ============================================================================
# 7. ANÁLISE DE DRAFT (CAMPEÕES)
# ============================================================================
print("\n" + "=" * 80)
print("7. ANÁLISE DE DRAFT")
print("=" * 80)

# Carregar dados de jogadores para análise de campeões
df_players = pd.read_parquet(os.path.join(data_dir, "lol_esports_players.parquet"))

# Win rate por campeão (mínimo 100 partidas)
champ_stats = df_players.groupby('champion').agg({
    'gameid': 'count',
    'result': 'mean'
}).rename(columns={'gameid': 'games', 'result': 'winrate'})
champ_stats['winrate'] = (champ_stats['winrate'] * 100).round(1)
champ_stats = champ_stats[champ_stats['games'] >= 100].sort_values('winrate', ascending=False)

print("\nTop 20 campeões por win rate (min 100 partidas):")
print(champ_stats.head(20).to_string())

# Campeões mais jogados
most_played = champ_stats.sort_values('games', ascending=False).head(20)
print("\nTop 20 campeões mais jogados:")
print(most_played.to_string())

# Análise de bans
ban_cols = ['blue_ban1', 'blue_ban2', 'blue_ban3', 'blue_ban4', 'blue_ban5',
            'red_ban1', 'red_ban2', 'red_ban3', 'red_ban4', 'red_ban5']
all_bans = []
for col in ban_cols:
    if col in df_draft.columns:
        all_bans.extend(df_draft[col].dropna().tolist())

ban_counts = pd.Series(all_bans).value_counts()
print("\nTop 20 campeões mais banidos:")
print(ban_counts.head(20).to_string())

insights['champions'] = {
    'top_winrate': champ_stats.head(30).to_dict(),
    'most_played': most_played.to_dict(),
    'most_banned': ban_counts.head(30).to_dict()
}

# ============================================================================
# 8. ANÁLISE POR POSIÇÃO
# ============================================================================
print("\n" + "=" * 80)
print("8. ANÁLISE POR POSIÇÃO")
print("=" * 80)

positions = ['top', 'jng', 'mid', 'bot', 'sup']
for pos in positions:
    pos_data = df_players[df_players['position'] == pos]
    top_champs = pos_data.groupby('champion').agg({
        'gameid': 'count',
        'result': 'mean'
    }).rename(columns={'gameid': 'games', 'result': 'winrate'})
    top_champs['winrate'] = (top_champs['winrate'] * 100).round(1)
    top_champs = top_champs[top_champs['games'] >= 50].sort_values('games', ascending=False)
    
    print(f"\n{pos.upper()} - Top 10 campeões mais jogados:")
    print(top_champs.head(10).to_string())

# ============================================================================
# 9. VARIABILIDADE POR PATCH E META
# ============================================================================
print("\n" + "=" * 80)
print("9. VARIABILIDADE POR PATCH E META")
print("=" * 80)

# Diversidade de campeões por ano
champ_diversity = df_players.groupby('year')['champion'].nunique()
print("\nDiversidade de campeões por ano:")
print(champ_diversity.to_string())

# Duração média por patch (últimos 2 anos)
recent_data = df_matches[df_matches['year'] >= 2024]
duration_by_patch = recent_data.groupby('patch')['gamelength'].mean() / 60
print("\nDuração média (min) por patch (2024+):")
print(duration_by_patch.round(1).to_string())

insights['variability'] = {
    'champion_diversity_by_year': champ_diversity.to_dict(),
    'duration_by_recent_patch': duration_by_patch.round(1).to_dict()
}

# ============================================================================
# SALVAR INSIGHTS
# ============================================================================
print("\n" + "=" * 80)
print("SALVANDO INSIGHTS")
print("=" * 80)

# Converter para tipos serializáveis
def convert_to_serializable(obj):
    if isinstance(obj, dict):
        return {str(k): convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    else:
        return obj

insights_serializable = convert_to_serializable(insights)

with open(os.path.join(output_dir, "insights.json"), "w") as f:
    json.dump(insights_serializable, f, indent=2, default=str)

print("Insights salvos em analysis/insights.json")
print("\nAnálise exploratória concluída!")
