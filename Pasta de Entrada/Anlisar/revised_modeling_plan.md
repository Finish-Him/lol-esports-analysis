# Plano de Ação Revisado: Modelo Preditivo Contextual para LoL Esports

**Data:** 18 de janeiro de 2026

## 1. Visão Geral e Objetivo

Este documento revisa o plano de ação para a construção de um modelo preditivo para partidas de League of Legends (LoL) Esports. A nova abordagem, alinhada com seu feedback, abandona a estratégia de treinar um modelo único com dados históricos massivos. Em vez disso, focaremos na criação de um **framework de modelagem contextual e dinâmico**.

O objetivo principal é construir modelos que sejam altamente sensíveis às condições atuais do jogo, considerando que o meta, a performance de jogadores e as estratégias de times mudam drasticamente de **patch para patch, de temporada para temporada e de região para região**.

## 2. Organização dos Dados (Fase Concluída)

Para suportar esta nova abordagem, os dados foram processados e organizados da seguinte forma:

-   **Parquet Geral:** Um arquivo (`lol_esports_ALL_YEARS.parquet`) contendo a totalidade dos dados brutos, servindo como base para cálculos históricos amplos.
-   **Parquet por Ano:** Arquivos individuais para cada ano (e.g., `lol_esports_2024.parquet`), permitindo o carregamento rápido e eficiente de dados para uma temporada específica.
-   **JSON e Markdown por Ano:** Relatórios detalhados e dados agregados para cada ano, fornecendo estatísticas sobre patches, ligas, times, jogadores e campeões, ideais para análise exploratória e validação de hipóteses.

Essa estrutura nos permite carregar apenas os dados relevantes para um determinado contexto, tornando o processo de treinamento e engenharia de features muito mais ágil e preciso.

## 3. Estratégia de Modelagem Contextual

A nova estratégia se baseia em treinar modelos sob demanda, utilizando janelas de dados relevantes para a partida que se deseja prever.

### 3.1. Engenharia de Features Dinâmica

As features não serão mais estáticas; elas serão calculadas dinamicamente com base no contexto da partida a ser prevista. Isso é crucial para capturar a performance e as tendências recentes.

| Categoria de Feature | Exemplos de Features Dinâmicas | Janelas de Tempo Sugeridas | Fonte de Dados Primária |
| :--- | :--- | :--- | :--- |
| **Performance Recente do Time** | - Win rate, KDA, GPM, DPM, controle de objetivos.<br>- Performance contra arquétipos de composição (e.g., poke, dive). | - **Patch Atual:** A mais importante.<br>- **Últimos 30/60 dias:** Captura a forma atual.<br>- **Split/Temporada Atual:** Performance geral na competição. | `Parquet por Ano` |
| **Performance Recente do Jogador** | - Win rate e KDA com campeões específicos.<br>- Champion pool recente e diversidade.<br>- Performance em confrontos de lane (CSD@10, XPD@10). | - **Patch Atual:** Relevância máxima.<br>- **Últimos 10-20 jogos competitivos:** Forma individual. | `Parquet por Ano` |
| **Meta do Patch** | - Win rate, pick rate, ban rate do campeão **no patch atual e na região específica**.<br>- Prioridade de objetivos (taxa de first dragon/herald) no patch.<br>- Sinergias e counter-picks emergentes no meta. | - **Patch Atual:** Apenas dados do patch vigente. | `Parquet por Ano` |
| **Contexto da Partida** | - Importância da partida (e.g., playoffs vs. fase regular).<br>- Histórico de confrontos diretos na temporada.<br>- Performance histórica da região em confrontos internacionais. | - **Split/Temporada Atual:** Para contexto competitivo. | `Parquet por Ano` |

### 3.2. Estratégia de Treinamento e Validação

Abandonaremos a divisão fixa de treino/validação/teste. Em vez disso, para cada partida que quisermos prever, aplicaremos uma **janela de treinamento deslizante (rolling window)**.

**Exemplo de Cenário:** Prever uma partida do Mundial (Worlds) 2025 no patch 15.20.

1.  **Seleção de Dados de Treinamento:**
    -   **Dados Primários:** Todas as partidas do Mundial 2025 até a data do jogo a ser previsto.
    -   **Dados Secundários:** Todas as partidas de ligas Tier 1 (LCK, LPL, LEC, LCS) jogadas no patch 15.20.
    -   **Dados Terciários (Opcional):** Partidas da segunda metade da temporada 2025 (Summer Split) para features de performance mais longas.

2.  **Geração de Features:** As features (win rate, KDA, etc.) para cada time e jogador seriam calculadas usando **apenas** os dados selecionados no passo 1.

3.  **Treinamento do Modelo:** Um modelo (e.g., XGBoost) é treinado do zero usando este conjunto de dados específico e contextual.

4.  **Previsão:** O modelo treinado é usado para prever o resultado da partida de interesse.

Este processo é repetido para cada nova previsão, garantindo que o modelo seja sempre o mais atualizado e contextualmente relevante possível.

### 3.3. Modelos a Serem Utilizados

-   **Gradient Boosting (LightGBM/XGBoost):** Continua sendo a escolha principal devido à sua performance excepcional em dados tabulares e sua capacidade de lidar com interações complexas.
-   **Modelos por Especialidade:** Podemos considerar treinar modelos especialistas. Por exemplo:
    -   Um modelo focado em prever o **early game** (e.g., first blood, first tower) usando features pré-jogo (draft, histórico dos jogadores).
    -   Um modelo que atualiza as previsões em tempo real (se dados ao vivo estiverem disponíveis) com base no estado do jogo (diferença de ouro, objetivos conquistados).

## 4. Próximos Passos e Implementação

1.  **Desenvolver a Biblioteca de Features:** Criar um conjunto de funções reutilizáveis para calcular as features dinâmicas descritas, aceitando um DataFrame de pandas (com dados de uma janela de tempo) como entrada.

2.  **Criar o Pipeline de Treinamento:** Desenvolver um script que orquestre o processo: selecionar os dados da janela de tempo, gerar as features, treinar o modelo e fazer a previsão.

3.  **Backtesting Rigoroso:** Simular o processo de previsão para temporadas passadas (e.g., usar dados até o final de 2024 para prever as partidas de 2025) para validar a robustez e a acurácia da estratégia.

4.  **Análise de Resultados e Iteração:** Analisar as previsões do backtesting para identificar pontos fracos e refinar a seleção de features e a estratégia de treinamento.

Esta abordagem contextual é computacionalmente mais intensiva, mas reflete com muito mais fidelidade a natureza do LoL competitivo, prometendo um modelo preditivo significativamente mais preciso e relevante e preciso.
