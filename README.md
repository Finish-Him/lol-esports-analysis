# 🎮 LoL Esports Data Analysis & Prediction

<div align="center">

![League of Legends](https://img.shields.io/badge/League%20of%20Legends-Esports-blue?style=for-the-badge&logo=riotgames&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-green?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Parquet](https://img.shields.io/badge/Apache%20Parquet-Storage-50ABF1?style=for-the-badge&logo=apache&logoColor=white)

**Análise completa e modelagem preditiva de partidas profissionais de League of Legends**

[📊 Dados](#-dados) • [🐍 Scripts](#-scripts-python) • [🤖 Modelagem](#-modelagem-preditiva) • [📈 Insights](#-principais-insights) • [🚀 Como Usar](#-como-usar)

</div>

---

## 📋 Sobre o Projeto

Este projeto consolida e analisa **13 anos de dados** de partidas profissionais de League of Legends (2014-2026), provenientes do [Oracle's Elixir](https://oracleselixir.com/), uma das fontes mais confiáveis de estatísticas do cenário competitivo de LoL.

### 🎯 Objetivos

- **Consolidação de Dados**: Unificar dados históricos de múltiplas temporadas em formatos otimizados
- **Análise Exploratória**: Identificar tendências, padrões de meta e estatísticas relevantes
- **Modelagem Preditiva**: Desenvolver modelos para prever resultados de partidas, duração de jogos e controle de objetivos
- **Geração de Relatórios**: Criar documentação automatizada em JSON e Markdown

---

## 📊 Dados

### Estatísticas do Dataset

| Métrica | Valor |
|---------|-------|
| 📁 **Total de Registros** | 1.123.176 |
| 🎮 **Partidas Analisadas** | 93.598 |
| 🏆 **Ligas/Campeonatos** | 120 |
| 👥 **Times** | 2.323 |
| 🎯 **Jogadores** | 11.006 |
| 🦸 **Campeões** | 172 |
| 🔧 **Patches** | 263 |
| 📅 **Período** | 2014 - 2026 |

### Estrutura de Pastas

```
📁 LOL/
├── 📁 Data/
│   ├── 📁 CSV/Todas as Partidas/    # Dados brutos por ano (Oracle's Elixir)
│   │   ├── 2014_LoL_esports_match_data_from_OraclesElixir.csv
│   │   ├── 2015_LoL_esports_match_data_from_OraclesElixir.csv
│   │   └── ... (até 2026)
│   │
│   ├── 📁 JSON/                      # Estatísticas agregadas por ano
│   │   ├── lol_esports_2014.json
│   │   └── ... (até 2026)
│   │
│   ├── 📁 Markdown/                  # Relatórios legíveis por humanos
│   │   ├── lol_esports_2014.md
│   │   └── ... (até 2026)
│   │
│   └── 📁 parquet/                   # Formato binário otimizado
│       ├── lol_esports_YEAR.parquet
│       └── lol_esports_ALL_YEARS.parquet
│
├── 📁 python/                        # Scripts de processamento
├── 📁 Pasta de Entrada/              # Inputs e planos de análise
│   └── 📁 Anlisar/                   # Documentação de modelagem
├── 📁 Imagens/                       # Visualizações e gráficos
└── 📁 Zip/                           # Arquivos compactados
```

### Schema dos Dados (130+ colunas)

<details>
<summary><b>🔍 Clique para expandir o schema completo</b></summary>

#### Identificação da Partida
| Coluna | Descrição |
|--------|-----------|
| `gameid` | ID único da partida |
| `league` | Liga/Campeonato |
| `year` | Ano da partida |
| `split` | Split (Spring/Summer/etc) |
| `playoffs` | Se é fase de playoffs |
| `date` | Data da partida |
| `game` | Número do jogo na série |
| `patch` | Versão do patch |

#### Informações do Participante
| Coluna | Descrição |
|--------|-----------|
| `participantid` | ID do participante (1-10) |
| `side` | Lado (Blue/Red) |
| `position` | Posição (top/jng/mid/bot/sup) |
| `playername` | Nome do jogador |
| `teamname` | Nome do time |
| `champion` | Campeão utilizado |

#### Draft (Banimentos e Picks)
| Coluna | Descrição |
|--------|-----------|
| `ban1` - `ban5` | Campeões banidos |
| `pick1` - `pick5` | Ordem de pick |

#### Resultados da Partida
| Coluna | Descrição |
|--------|-----------|
| `gamelength` | Duração do jogo (segundos) |
| `result` | Resultado (1=vitória, 0=derrota) |
| `kills` | Abates |
| `deaths` | Mortes |
| `assists` | Assistências |
| `teamkills` | Total de abates do time |

#### Primeiros Objetivos
| Coluna | Descrição |
|--------|-----------|
| `firstblood` | Primeiro sangue |
| `firstdragon` | Primeiro dragão |
| `firstherald` | Primeiro arauto |
| `firstbaron` | Primeiro Baron |
| `firsttower` | Primeira torre |

#### Objetivos Totais
| Coluna | Descrição |
|--------|-----------|
| `dragons` | Total de dragões |
| `barons` | Total de Barons |
| `towers` | Total de torres |
| `inhibitors` | Total de inibidores |
| `heralds` | Total de arautos |
| `void_grubs` | Void Grubs (novo objetivo) |
| `atakhans` | Atakhans (novo objetivo) |

#### Economia
| Coluna | Descrição |
|--------|-----------|
| `totalgold` | Ouro total |
| `earnedgold` | Ouro ganho |
| `goldat10/15/20/25` | Ouro aos 10/15/20/25 min |
| `xpat10/15/20/25` | XP aos 10/15/20/25 min |
| `csat10/15/20/25` | CS aos 10/15/20/25 min |

#### Estatísticas de Combate
| Coluna | Descrição |
|--------|-----------|
| `damagetochampions` | Dano total a campeões |
| `dpm` | Dano por minuto |
| `damageshare` | % do dano do time |
| `damagetakenperminute` | Dano recebido por min |

#### Visão
| Coluna | Descrição |
|--------|-----------|
| `wardsplaced` | Wards colocadas |
| `wardskilled` | Wards destruídas |
| `controlwardsbought` | Control wards compradas |
| `visionscore` | Score de visão |

</details>

---

## 🐍 Scripts Python

| Script | Descrição |
|--------|-----------|
| [`consolidate_data.py`](python/consolidate_data.py) | 🔄 Script principal de consolidação - mescla todos os CSVs e cria datasets Parquet para times, jogadores, partidas e draft |
| [`consolidate_optimized.py`](python/consolidate_optimized.py) | ⚡ Versão otimizada com processamento em chunks para economia de memória |
| [`create_all_files.py`](python/create_all_files.py) | 📦 Pipeline completo - cria Parquet, JSON e Markdown para todos os anos |
| [`complete_missing_files.py`](python/complete_missing_files.py) | 🔧 Gera arquivos faltantes para anos recentes (2024-2026) |
| [`detailed_analysis.py`](python/detailed_analysis.py) | 🔬 Análise profunda da estrutura do dataset, completude e variáveis alvo |
| [`exploratory_analysis.py`](python/exploratory_analysis.py) | 📊 Gera insights sobre tendências temporais, vantagem de lado, ligas, objetivos |
| [`explore_data.py`](python/explore_data.py) | 🔍 Exploração inicial e análise da estrutura de colunas |
| [`optimized_analysis.py`](python/optimized_analysis.py) | 🚀 Análise eficiente usando apenas colunas essenciais |
| [`separate_by_year.py`](python/separate_by_year.py) | 📅 Separa o dataset consolidado por ano |

---

## 🤖 Modelagem Preditiva

### Objetivos de Predição

| Target | Tipo | Descrição |
|--------|------|-----------|
| 🏆 **Vencedor da Partida** | Classificação Binária | Prever qual time (Blue/Red) vencerá |
| ⏱️ **Duração do Jogo** | Regressão | Prever `gamelength` em segundos |
| 🐉 **Controle de Objetivos** | Classificação/Regressão | Primeiro dragão, total de dragões, etc. |

### Estratégia de Modelagem

O projeto utiliza uma abordagem **contextual/dinâmica** com rolling windows que considera:

- 📋 **Meta atual** do patch
- 📈 **Performance recente** do time/jogador (últimos 30/60/90 dias)
- 🌍 **Diferenças regionais** entre ligas
- 🏆 **Contexto do torneio** (fase de grupos vs playoffs)

### Modelos Propostos

```
┌─────────────────────────────────────────────────────────────┐
│  Baseline        │  Avançados              │  Opcional      │
├─────────────────────────────────────────────────────────────┤
│  Logistic        │  XGBoost                │  Neural        │
│  Regression      │  LightGBM               │  Networks      │
│                  │  (Gradient Boosting)    │  (Draft AI)    │
└─────────────────────────────────────────────────────────────┘
```

### Features a Serem Engenheiradas

<details>
<summary><b>📐 Clique para ver features propostas</b></summary>

#### Features de Time
- Win rate geral, recente e por patch
- Performance em Blue/Red side
- Média de duração das partidas
- Taxa de first blood/dragon/baron

#### Features de Jogador
- KDA médio (geral e por campeão)
- Champion pool e win rate por campeão
- Performance de lane (CSD@10, XPD@10, GD@10)
- Tendência de farm vs agressividade

#### Features de Draft
- Win rate dos campeões no patch atual
- Taxa de pick/ban
- Sinergias de composição
- Counter-picks históricos

#### Features Contextuais
- Head-to-head histórico entre times
- Performance no torneio atual
- Importância da partida (eliminatória vs fase de grupos)

</details>

### Divisão dos Dados

```
┌────────────────────────────────────────────────────────────────────┐
│ 2014-2023          │ 2024              │ 2025-2026                 │
│ TREINO             │ VALIDAÇÃO         │ TESTE                     │
│ ~85% dos dados     │ ~8% dos dados     │ ~7% dos dados             │
└────────────────────────────────────────────────────────────────────┘
```

---

## 📈 Principais Insights

### Vantagem de Lado (Blue vs Red)

```
Blue Side Win Rate: 53.2%  ████████████████████░░░░░
Red Side Win Rate:  46.8%  █████████████████░░░░░░░░
```

> O lado azul mantém uma vantagem histórica consistente devido ao primeiro pick no draft.

### Evolução da Duração das Partidas

| Ano | Duração Média |
|-----|---------------|
| 2014 | 38.1 min |
| 2016 | 36.8 min |
| 2018 | 33.5 min |
| 2020 | 32.1 min |
| 2022 | 31.5 min |
| 2024 | 31.2 min |
| 2026 | 31.8 min |

> 📉 Tendência de queda na duração das partidas ao longo dos anos, indicando meta mais agressiva.

### Top Ligas por Volume de Partidas

| # | Liga | Partidas |
|---|------|----------|
| 1 | 🇨🇳 LDL | 7.033 |
| 2 | 🇨🇳 LPL | 6.754 |
| 3 | 🇰🇷 LCK | 5.000 |
| 4 | 🇹🇷 TCL | 2.438 |
| 5 | 🇻🇳 VCS | 2.374 |

---

## 🚀 Como Usar

### Pré-requisitos

```bash
# Python 3.8+
python --version

# Instalar dependências
pip install pandas numpy pyarrow
```

### Carregar os Dados

```python
import pandas as pd

# Carregar dataset completo (Parquet - recomendado)
df = pd.read_parquet('Data/parquet/lol_esports_ALL_YEARS.parquet')

# Carregar ano específico
df_2025 = pd.read_parquet('Data/parquet/lol_esports_2025.parquet')

# Ou via CSV
df_csv = pd.read_csv('Data/CSV/Todas as Partidas/2025_LoL_esports_match_data_from_OraclesElixir.csv')
```

### Filtrar Dados de Times

```python
# Filtrar apenas linhas de times (não jogadores individuais)
teams_df = df[df['participantid'].isin([100, 200])]

# Estatísticas de um time específico
t1_stats = teams_df[teams_df['teamname'] == 'T1']
print(f"Win Rate T1: {t1_stats['result'].mean():.1%}")
```

### Analisar um Patch Específico

```python
# Filtrar por patch
patch_1401 = df[df['patch'] == '14.01']

# Win rate por lado no patch
blue_wr = patch_1401[patch_1401['side'] == 'Blue']['result'].mean()
print(f"Blue Side Win Rate (14.01): {blue_wr:.1%}")
```

### Executar Scripts

```bash
# Consolidar todos os dados
python python/consolidate_data.py

# Gerar relatórios JSON e Markdown
python python/create_all_files.py

# Análise exploratória
python python/exploratory_analysis.py
```

---

## 📁 Formatos de Saída

| Formato | Uso Recomendado | Vantagens |
|---------|-----------------|-----------|
| **Parquet** | Data Science, ML | Compressão eficiente, leitura rápida, tipagem preservada |
| **JSON** | APIs, Integração | Estruturado, fácil parsing, interoperável |
| **Markdown** | Documentação | Legível, versionável, apresentável |
| **CSV** | Dados brutos | Universal, editável, compatível |

---

## 📊 Status do Projeto

- [x] ✅ Consolidação de dados (2014-2026)
- [x] ✅ Análise exploratória completa
- [x] ✅ Geração de relatórios JSON/Markdown
- [x] ✅ Documentação do plano de modelagem
- [ ] 🔄 Feature engineering
- [ ] 🔄 Treinamento de modelos
- [ ] 🔄 Backtesting framework
- [ ] 🔄 API de predições

---

## 🛠️ Tecnologias Utilizadas

<div align="center">

| Categoria | Tecnologias |
|-----------|-------------|
| **Linguagem** | Python 3.x |
| **Manipulação de Dados** | Pandas, NumPy |
| **Armazenamento** | Apache Parquet, JSON |
| **ML (Planejado)** | XGBoost, LightGBM, Scikit-learn |
| **Interpretabilidade** | SHAP |

</div>

---

## 📚 Referências

- [Oracle's Elixir](https://oracleselixir.com/) - Fonte primária dos dados
- [LoL Esports](https://lolesports.com/) - Calendário e informações oficiais
- [Leaguepedia](https://lol.fandom.com/) - Wiki de LoL Esports

---

## 📄 Licença

Este projeto utiliza dados públicos do Oracle's Elixir para fins educacionais e de pesquisa.

---

<div align="center">

**Feito com ❤️ para a comunidade de LoL Esports**

⭐ Star este repositório se foi útil!

</div>
