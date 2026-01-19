# Roteiro de Arquivos Markdown - LoL Esports Analysis

---

![Status](https://img.shields.io/badge/Status-Planejamento-yellow?style=for-the-badge)
![Arquivos](https://img.shields.io/badge/Arquivos_Planejados-45+-blue?style=for-the-badge)

*Ultima Atualizacao: 19 de Janeiro de 2026*

---

# Resumo do Projeto

## Arquivos Existentes (34 arquivos)

| Categoria | Quantidade | Arquivos |
|-----------|------------|----------|
| **INDEX** | 1 | INDEX.md |
| **Ligas 2026** | 10 | LCK, LEC, LPL, CBLOL, AL, HLL, LCKC, LCP, LIT, NLC, ROL |
| **Composicoes** | 3 | LCK, LEC, LPL Compositions |
| **Insights** | 1 | LCK_Insights_2026 |
| **Players** | 1 | LCK_Players |
| **Meta** | 2 | Champion_Power_Index, Champions |
| **Global** | 1 | Global_Regional_Comparison |
| **Anuais** | 13 | lol_esports_2014-2026 |
| **Raiz** | 2 | Champion_Meta_Report, README |

---

# ROTEIRO DE NOVOS ARQUIVOS

## Prioridade 1: Paridade Regional (Alta Prioridade)

Completar analises para todas as regioes principais no mesmo nivel de LCK.

### 1.1 LEC (Europa/EMEA)

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 1 | `Data/Ligas/LEC_Players.md` | Perfis de jogadores LEC 2022-2026 (Caps, Jankos, Humanoid, etc.) | JSON 2022-2026 | ~1000 |
| 2 | `Data/Ligas/LEC_Insights_2026.md` | Insights estrategicos, power rankings, meta analysis LEC | JSON 2025-2026 | ~700 |
| 3 | `Data/Ligas/LEC_Historical.md` | Historia da LEC/EU LCS 2014-2026 (Worlds, MSI, evolucao) | JSON todos | ~800 |

### 1.2 LPL (China)

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 4 | `Data/Ligas/LPL_Players.md` | Perfis de jogadores LPL 2022-2026 (TheShy, Xiaohu, JackeyLove, etc.) | JSON 2022-2026 | ~1200 |
| 5 | `Data/Ligas/LPL_Insights_2026.md` | Insights estrategicos, power rankings, meta analysis LPL | JSON 2025-2026 | ~700 |

### 1.3 Americas (LCS/LTA)

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 6 | `Data/Ligas/LCS_2026.md` | Relatorio completo LCS/Americas 2026 | JSON 2026 | ~400 |
| 7 | `Data/Ligas/LCS_Players.md` | Perfis de jogadores NA 2022-2026 (Doublelift legacy, novos talentos) | JSON 2022-2026 | ~800 |
| 8 | `Data/Ligas/LCS_Historical.md` | Historia da LCS 2014-2026 | JSON todos | ~600 |

---

## Prioridade 2: Ligas Secundarias (Media Prioridade)

Expandir cobertura para ligas regionais importantes.

### 2.1 Asia-Pacifico

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 9 | `Data/Ligas/VCS_2026.md` | Vietnam Championship Series 2026 | JSON 2025-2026 | ~400 |
| 10 | `Data/Ligas/PCS_2026.md` | Pacific Championship Series 2026 (Taiwan/SEA) | JSON 2025-2026 | ~400 |
| 11 | `Data/Ligas/LJL_2026.md` | League of Legends Japan League 2026 | JSON 2025-2026 | ~350 |

### 2.2 Turquia e Outras

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 12 | `Data/Ligas/TCL_2026.md` | Turkish Championship League 2026 | JSON 2025-2026 | ~350 |
| 13 | `Data/Ligas/LCO_2026.md` | League of Legends Circuit Oceania 2026 | JSON 2025-2026 | ~300 |

### 2.3 Americas Latinas

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 14 | `Data/Ligas/CBLOL_Players.md` | Perfis de jogadores brasileiros (brTT, Robo, etc.) | JSON 2022-2026 | ~600 |
| 15 | `Data/Ligas/CBLOL_Historical.md` | Historia do CBLOL 2014-2026 | JSON todos | ~500 |
| 16 | `Data/Ligas/LLA_2026.md` | Liga Latinoamerica 2026 | JSON 2025-2026 | ~350 |

---

## Prioridade 3: Analises Especializadas (Alta Prioridade)

### 3.1 Analises de Times

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 17 | `Data/Times/T1_Complete.md` | Analise completa T1 2014-2026 (historia, roster, titulos) | JSON todos | ~1500 |
| 18 | `Data/Times/GenG_Complete.md` | Analise completa Gen.G/Samsung 2014-2026 | JSON todos | ~1200 |
| 19 | `Data/Times/G2_Complete.md` | Analise completa G2 Esports 2015-2026 | JSON 2015-2026 | ~1000 |
| 20 | `Data/Times/Top_Teams_Global.md` | Top 20 times historicos (titulos, legacy) | JSON todos | ~800 |

### 3.2 Mundiais e Eventos Internacionais

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 21 | `Data/Eventos/Worlds_History.md` | Todos os Worlds 2014-2025 (campeoes, meta, stats) | JSON todos | ~1500 |
| 22 | `Data/Eventos/MSI_History.md` | Todos os MSI 2015-2025 | JSON 2015-2025 | ~800 |
| 23 | `Data/Eventos/International_Stats.md` | Estatisticas comparativas internacionais | JSON todos | ~600 |

### 3.3 Analises de Objetivos

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 24 | `Data/Meta/Objectives_Analysis.md` | Analise de objetivos: Dragons, Barons, Heralds, Grubs | JSON 2024-2026 | ~700 |
| 25 | `Data/Meta/First_Blood_Analysis.md` | Impacto de First Blood por regiao/liga | JSON 2024-2026 | ~500 |
| 26 | `Data/Meta/Game_Duration_Trends.md` | Tendencias de duracao de partidas 2014-2026 | JSON todos | ~600 |

---

## Prioridade 4: Evolucao e Historico (Media Prioridade)

### 4.1 Evolucao do Meta

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 27 | `Data/Meta/Meta_Evolution_2014-2026.md` | Evolucao do meta ao longo dos anos | JSON todos | ~1200 |
| 28 | `Data/Meta/Patch_Impact_Analysis.md` | Impacto de patches significativos no meta | JSON 2020-2026 | ~800 |
| 29 | `Data/Meta/Role_Evolution.md` | Evolucao de cada role (Top/Jg/Mid/ADC/Sup) | JSON todos | ~1000 |

### 4.2 Analises de Campeoes Especificos

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 30 | `Data/Meta/Champion_Azir.md` | Analise completa Azir (pick/ban, winrate, regioes) | JSON 2014-2026 | ~400 |
| 31 | `Data/Meta/Champion_Ksante.md` | Analise completa K'Sante (lancamento ate hoje) | JSON 2022-2026 | ~400 |
| 32 | `Data/Meta/Champion_LeeSin.md` | Analise completa Lee Sin (presenca pro play) | JSON 2014-2026 | ~400 |
| 33 | `Data/Meta/Flex_Picks_Analysis.md` | Analise de flex picks por temporada | JSON 2020-2026 | ~600 |

---

## Prioridade 5: Guias e Recursos (Baixa Prioridade)

### 5.1 Guias Praticos

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 34 | `Data/Guias/Betting_Guide_Complete.md` | Guia completo de apostas esportivas LoL | JSON 2024-2026 | ~800 |
| 35 | `Data/Guias/Draft_Analysis_Guide.md` | Como analisar drafts (prioridades, counters) | JSON 2024-2026 | ~600 |
| 36 | `Data/Guias/Stats_Glossary.md` | Glossario de estatisticas (KDA, CS/min, etc.) | - | ~300 |

### 5.2 Comparativos

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 37 | `Data/Ligas/Minor_Leagues_Comparison.md` | Comparativo entre ligas menores | JSON 2025-2026 | ~500 |
| 38 | `Data/Ligas/Academy_Leagues.md` | Analise de ligas academy (LCKC, LDL, NACL) | JSON 2024-2026 | ~600 |

---

## Prioridade 6: Dashboards e Indices (Baixa Prioridade)

| # | Arquivo | Descricao | Dados Fonte | Linhas Est. |
|---|---------|-----------|-------------|-------------|
| 39 | `Data/Dashboards/Quick_Stats_2026.md` | Dashboard rapido com stats atuais | JSON 2026 | ~300 |
| 40 | `Data/Dashboards/Weekly_Update.md` | Template para atualizacoes semanais | JSON atual | ~200 |

---

# CORRECOES PENDENTES

Antes de criar novos arquivos, corrigir issues existentes:

| # | Arquivo | Issue | Acao |
|---|---------|-------|------|
| 1 | `Data/INDEX.md` | Champion_Power_Index nao esta linkado | Adicionar link na secao Meta |
| 2 | `Data/INDEX.md` | Falta link para LPL.md | Verificar e adicionar |

---

# RESUMO POR CATEGORIA

| Categoria | Arquivos Existentes | Arquivos Planejados | Total |
|-----------|---------------------|---------------------|-------|
| **Ligas** | 11 | 11 | 22 |
| **Players** | 1 | 4 | 5 |
| **Insights** | 1 | 2 | 3 |
| **Composicoes** | 3 | 0 | 3 |
| **Times** | 0 | 4 | 4 |
| **Eventos** | 0 | 3 | 3 |
| **Meta** | 2 | 10 | 12 |
| **Guias** | 0 | 3 | 3 |
| **Dashboards** | 1 | 2 | 3 |
| **TOTAL** | 34 | 40 | 74 |

---

# ORDEM DE EXECUCAO SUGERIDA

## Fase 1: Fundacao (Proximos 5 arquivos)
1. Corrigir INDEX.md (links faltando)
2. LEC_Players.md
3. LPL_Players.md
4. LEC_Insights_2026.md
5. LPL_Insights_2026.md

## Fase 2: Expansao Regional (Proximos 8 arquivos)
6. LCS_2026.md
7. VCS_2026.md
8. PCS_2026.md
9. TCL_2026.md
10. LJL_2026.md
11. LCS_Players.md
12. CBLOL_Players.md
13. LLA_2026.md

## Fase 3: Historia e Times (Proximos 7 arquivos)
14. T1_Complete.md
15. GenG_Complete.md
16. G2_Complete.md
17. Worlds_History.md
18. MSI_History.md
19. LEC_Historical.md
20. LCS_Historical.md

## Fase 4: Meta e Analises (Proximos 10 arquivos)
21. Meta_Evolution_2014-2026.md
22. Objectives_Analysis.md
23. Game_Duration_Trends.md
24. Patch_Impact_Analysis.md
25. Role_Evolution.md
26. Flex_Picks_Analysis.md
27. Champion_Azir.md
28. Champion_Ksante.md
29. Champion_LeeSin.md
30. First_Blood_Analysis.md

## Fase 5: Complementos (Ultimos 10 arquivos)
31-40. Guias, Dashboards, Ligas Menores

---

# ESTRUTURA DE PASTAS PROPOSTA

```
Data/
├── INDEX.md
├── Ligas/                    # Relatorios por liga
│   ├── LCK_2026.md
│   ├── LEC_2026.md
│   ├── LPL.md
│   ├── LCK_Players.md
│   ├── LEC_Players.md        # NOVO
│   ├── LPL_Players.md        # NOVO
│   └── ...
├── Times/                    # NOVA PASTA
│   ├── T1_Complete.md
│   ├── GenG_Complete.md
│   └── ...
├── Eventos/                  # NOVA PASTA
│   ├── Worlds_History.md
│   ├── MSI_History.md
│   └── ...
├── Meta/
│   ├── Champion_Power_Index.md
│   ├── Champions.md
│   ├── Meta_Evolution.md     # NOVO
│   └── ...
├── Guias/                    # NOVA PASTA
│   ├── Betting_Guide.md
│   └── ...
├── Dashboards/               # NOVA PASTA
│   └── Quick_Stats.md
├── JSON/
├── Markdown/
└── parquet/
```

---

# DADOS DISPONIVEIS PARA USO

| Fonte | Anos | Partidas | Times | Jogadores | Campeoes |
|-------|------|----------|-------|-----------|----------|
| JSON | 2014-2026 | 93.598 | 2.323 | 11.006 | 172 |
| Ligas | 45+ | - | - | - | - |
| Patches | 263 | - | - | - | - |

## Ligas Principais nos Dados

| Liga | 2024 Partidas | 2025 Partidas | Cobertura |
|------|---------------|---------------|-----------|
| LPL | 717 | 805 | Completa |
| LCK | 482 | 678 | Completa |
| LEC | 294 | 400+ | Completa |
| LCKC | 511 | 450+ | Parcial |
| LDL | 565 | 500+ | Minima |
| NACL | 488 | 400+ | Minima |
| VCS | 252 | 300+ | Minima |
| CBLOL | 263 | 350+ | Parcial |
| TCL | 181 | 200+ | Minima |

---

*Roteiro criado em 19 de Janeiro de 2026*
*Total de arquivos planejados: 40 novos arquivos*
*Estimativa total de linhas: ~25.000 linhas de conteudo*
