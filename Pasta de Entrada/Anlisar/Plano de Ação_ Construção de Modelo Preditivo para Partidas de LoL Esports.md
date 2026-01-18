# Plano de Ação: Construção de Modelo Preditivo para Partidas de LoL Esports

**Data:** 18 de janeiro de 2026

## 1. Introdução

Este documento detalha o plano de ação para a construção de um modelo preditivo robusto para partidas de League of Legends (LoL) Esports. O objetivo é utilizar o vasto conjunto de dados históricos (2014-2026) para prever diversos aspectos de uma partida, como o vencedor, a duração e o controle de objetivos. A estratégia central se baseia na criação de features complexas e na ponderação de dados recentes para refletir a natureza dinâmica e evolutiva do jogo.

## 2. Análise Exploratória e Consolidação de Dados (Fase Concluída)

Na fase inicial, realizamos uma análise aprofundada dos 13 anos de dados fornecidos. O processo incluiu:

- **Análise de Estrutura:** Verificação da consistência das colunas e tipos de dados ao longo dos anos.
- **Consolidação:** Unificação de todos os arquivos CSV em formatos otimizados (Parquet) para performance.
- **Criação de Datasets Específicos:** Geração de arquivos separados para jogadores, times, partidas (uma linha por jogo) e drafts, facilitando a engenharia de features.
- **Insights Iniciais:** Extração de estatísticas chave sobre win rate por lado, popularidade de campeões, tendências de duração de jogo e impacto de primeiros objetivos.

Os dados estão agora organizados e prontos para a próxima fase, armazenados no diretório `/home/ubuntu/lol_prediction_project/data/`.

## 3. Planejamento do Modelo Preditivo

O projeto será dividido em etapas sequenciais, desde a engenharia de features até a avaliação do modelo final.

### 3.1. Definição do Problema e Métricas de Sucesso

O projeto focará em três tarefas de predição principais:

1.  **Previsão do Vencedor:** Classificação binária (Time Azul vs. Time Vermelho).
    - **Métrica Primária:** Acurácia.
    - **Métrica Secundária:** Log Loss (para avaliar a confiança das previsões).

2.  **Previsão da Duração da Partida:** Regressão (prever `gamelength` em segundos).
    - **Métrica Primária:** Erro Absoluto Médio (MAE).
    - **Métrica Secundária:** Raiz do Erro Quadrático Médio (RMSE).

3.  **Previsão de Objetivos:** Regressão ou classificação, dependendo do objetivo.
    - **Exemplo:** Prever o número total de dragões (regressão) ou qual time obterá o primeiro dragão (classificação).
    - **Métricas:** MAE/RMSE para regressão, Acurácia/F1-Score para classificação.

### 3.2. Engenharia de Features (Feature Engineering)

Esta é a etapa mais crítica. Criaremos features que capturem o estado do jogo e a performance histórica de times e jogadores, com ênfase em dados recentes.

| Categoria de Feature | Descrição e Exemplos | Fonte de Dados | Importância | 
| :--- | :--- | :--- | :--- | 
| **Features de Times** | - Win rate geral e recente (últimos 10/20 jogos, patch atual).<br>- Média de KDA, Ouro por Minuto (GPM), Dano por Minuto (DPM).<br>- Taxas de controle de objetivos (Dragões, Barões, Torres).<br>- Performance histórica contra o oponente direto. | `lol_esports_teams.parquet` | Alta | 
| **Features de Jogadores** | - Win rate e KDA do jogador (geral e com campeão específico).<br>- Sinergia com o time (win rate do jogador na equipe atual).<br>- Champion pool (número de campeões únicos jogados). | `lol_esports_players.parquet` | Média | 
| **Features de Draft** | - Win rate do campeão no patch atual.<br>- Presença (Pick+Ban rate) do campeão.<br>- Sinergia de composição (e.g., win rate de campeões jogados juntos).<br>- Análise de counter-picks (baseado em dados históricos). | `lol_esports_draft.parquet` | Alta | 
| **Features de Meta** | - Estatísticas agregadas de campeões no patch atual (win rate, pick rate, ban rate).<br>- Duração média das partidas no patch.<br>- Prioridade de objetivos no patch (e.g., taxa de first dragon). | `lol_esports_matches.parquet` | Alta | 

**Estratégia de Ponderação Temporal:** Para dar mais peso a eventos recentes, as features de performance (win rate, KDA, etc.) serão calculadas em janelas de tempo móveis (e.g., últimos 30/60/90 dias, jogos no patch atual, jogos no split atual).

### 3.3. Seleção e Preparação dos Dados

- **Filtragem:** Inicialmente, focaremos em ligas de Tier 1 e Tier 2 para garantir a qualidade e a relevância competitiva dos dados. Ligas menores podem ser incluídas posteriormente.
- **Tratamento de Nulos:** Variáveis com alta porcentagem de valores nulos serão removidas ou tratadas com técnicas de imputação (média, mediana, etc.), dependendo do caso.
- **Divisão dos Dados:** Os dados serão divididos em conjuntos de **treino, validação e teste** de forma cronológica. Por exemplo:
    - **Treino:** 2014 - 2023
    - **Validação:** 2024
    - **Teste:** 2025 - 2026
  Isso previne o vazamento de dados (data leakage) e simula um cenário de previsão real.

### 3.4. Modelagem

1.  **Modelo de Baseline:** Iniciaremos com um modelo simples, como uma **Regressão Logística**, usando apenas features básicas (e.g., win rate histórico dos times) para estabelecer uma linha de base de performance.

2.  **Modelos Avançados:** Implementaremos modelos mais sofisticados que capturam interações complexas entre as features:
    - **Gradient Boosting (XGBoost, LightGBM):** São os modelos mais promissores para este tipo de dado tabular. São eficientes, escaláveis e geralmente oferecem a melhor performance.
    - **Redes Neurais:** Podem ser exploradas para capturar padrões não-lineares, especialmente em features de draft e sinergia de composição.

### 3.5. Avaliação e Iteração

- **Avaliação:** Os modelos serão avaliados no conjunto de teste usando as métricas definidas na seção 3.1.
- **Análise de Features:** Utilizaremos técnicas como SHAP (SHapley Additive exPlanations) para interpretar as previsões do modelo e entender quais features são mais impactantes. Isso gerará insights valiosos sobre o meta do jogo.
- **Ciclo de Iteração:** O processo será iterativo. Com base na análise de erros e na importância das features, retornaremos à etapa de engenharia de features para refinar o modelo, criar novas variáveis e melhorar a performance.

## 4. Próximos Passos

1.  **Implementação da Engenharia de Features:** Desenvolver os scripts para calcular todas as features definidas.
2.  **Treinamento do Modelo Baseline:** Criar e avaliar o primeiro modelo simples.
3.  **Treinamento dos Modelos Avançados:** Implementar e otimizar os modelos de Gradient Boosting.
4.  **Análise e Relatório Final:** Gerar o relatório final com os resultados, a análise de features e os insights obtidos.

Este plano fornece uma estrutura sólida para a construção de um modelo preditivo de alta qualidade, abordando os principais desafios do projeto, como a complexidade e a natureza evolutiva do League of Legends.
