# ⚽ Football Data Platform — End-to-End Data Engineering

> **Documento de continuidade do projeto** — versão baseada no domínio de futebol.  
> **Status:** arquitetura e roadmap definidos; implementação ainda não iniciada.

---

## 1. Objetivo

Construir uma plataforma de dados **end-to-end**, **open source** e **containerizada**, usando dados públicos de futebol.

O projeto deve demonstrar competências atuais de Data Engineering:

- Ingestion
- ELT
- Orchestration
- Modelagem dimensional
- Data Quality
- Testes
- Infrastructure as Code (IaC)
- CI/CD
- Security
- Data lineage
- Observability
- Analytics

A primeira versão será **100% local com Docker**. Depois que estiver estável, o projeto poderá ganhar uma segunda implementação em **AWS** para demonstrar competências de Cloud Data Engineering.

---

# 2. Domínio e dataset

## Dataset principal

**Football-Data.co.uk**, inicialmente com dados históricos da **Premier League**.

Características:

- Dados históricos de partidas
- Arquivos CSV
- Fácil de baixar e processar
- Resultados
- Dependendo da temporada, estatísticas e odds

## Fonte alternativa / expansão

**OpenFootball**

Objetivo futuro:

- Ampliar para outras ligas
- Adicionar competições
- Demonstrar integração de múltiplas fontes

### Estratégia inicial

Não complicar o projeto com várias fontes no início.

Começar com:

```text
Competition: Premier League
History: 1993 → atual
Format: CSV
Primary grain: one row per match
```

Depois expandir.

---

# 3. Stack definida

| Área | Tecnologia | Função |
|---|---|---|
| Versionamento | Git + GitHub | Código, PR, review e histórico |
| Containers | Docker + Docker Compose | Ambiente local reproduzível |
| Ingestion | Airbyte | Replicação/ingestion source → raw |
| Source | PostgreSQL | Banco que recebe o dataset original |
| Warehouse | PostgreSQL | Raw + staging + intermediate + marts |
| Transformation | dbt | ELT, modelagem e testes |
| Orchestration | Apache Airflow | Coordenação do pipeline |
| Python tests | Pytest | Testes unitários/integration |
| SQL quality | SQLFluff | Lint de SQL |
| Data quality | dbt tests + Great Expectations | Regras de qualidade e negócio |
| IaC | Terraform | Infra/configuração reproduzível |
| CI/CD | GitHub Actions | Automação de checks e deploy |
| Security | Trivy + secret scanning | Vulnerabilidades e secrets |
| Lineage | OpenLineage + Marquez | Lineage de jobs/datasets |
| BI | Metabase | Dashboards e consumo analítico |
| Tooling | pre-commit + Ruff + Makefile | Padronização local |

---

# 4. Arquitetura

## Fluxo principal

```text
                         Football-Data.co.uk
                                  │
                                  ▼
                         Python dataset loader
                                  │
                                  ▼
                         PostgreSQL SOURCE
                                  │
                                Airbyte
                                  │
                                  ▼
                         PostgreSQL DW / raw
                                  │
                                 dbt
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
           staging           intermediate           marts
                                                      │
                                      ┌───────────────┴───────────────┐
                                      ▼                               ▼
                               Team Analytics                   Match Analytics
                                      │                               │
                                      └───────────────┬───────────────┘
                                                      ▼
                                                   Metabase
```

## Orchestration

```text
Airflow
  ├── trigger Airbyte
  ├── wait for ingestion
  ├── run dbt
  ├── run dbt tests
  ├── run Great Expectations
  └── notify / finish
```

## CI/CD

```text
GitHub
  ↓
Pull Request
  ↓
GitHub Actions
  ├── pre-commit
  ├── Ruff
  ├── Pytest
  ├── SQLFluff
  ├── dbt parse / compile / test
  ├── Terraform fmt / validate / plan
  └── Trivy / secret scan
  ↓
Code review
  ↓
Merge
  ↓
CD / deployment
```

---

# 5. Modelo dimensional

## Modelo principal

```text
                    dim_team
                       │
                       │
dim_date ───────── fct_match ───────── dim_competition
                       │
                       │
                 dim_referee
```

### Dimensões opcionais futuras

```text
dim_stadium
dim_manager
dim_player
dim_country
```

## Fato principal — `fct_match`

```text
match_id
date_key
season_key
competition_key
home_team_key
away_team_key
referee_key
home_goals
away_goals
home_half_time_goals
away_half_time_goals
result
```

## Marts derivados

### `fct_team_season`

```text
team
season
matches
wins
draws
losses
goals_for
goals_against
goal_difference
points
```

### `fct_daily_metrics`

```text
date
matches
goals
avg_goals_per_match
home_win_pct
draw_pct
away_win_pct
```

---

# 6. Regras de negócio para demonstrar Data Quality

O domínio de futebol permite criar testes de negócio interessantes.

## Regras sugeridas

- `home_goals >= 0`
- `away_goals >= 0`
- `home_goals` e `away_goals` devem ser inteiros
- O resultado deve ser compatível com o placar:
  - `HOME` → mandante venceu
  - `DRAW` → empate
  - `AWAY` → visitante venceu
- `home_team` não pode ser `NULL`
- `away_team` não pode ser `NULL`
- `home_team != away_team`, salvo caso documentado de fonte
- `date` deve ser válida
- `season` deve ser consistente com a data
- `matches_played = wins + draws + losses`
- `points = 3 * wins + 1 * draws`
- `goals_for` e `goals_against` devem bater com os jogos agregados
- Chaves de dimensões devem existir
- Detectar duplicidade de `match_id`
- O volume esperado por temporada deve estar dentro de uma faixa razoável

Essas regras podem ser distribuídas entre:

- dbt tests
- dbt generic tests
- dbt custom tests
- Great Expectations
- Pytest, quando fizer sentido

---

# 7. Estratégia de ingestion

O dataset será primeiro carregado em um **PostgreSQL SOURCE**.

Isso cria um sistema de origem realista para o Airbyte consumir.

## Fluxo

```text
CSV / dataset
    ↓
Python loader
    ↓
PostgreSQL SOURCE
    ↓
Airbyte
    ↓
PostgreSQL DW.raw
```

## Responsabilidades

A transformação deve permanecer no dbt.

Regra principal:

> **Airbyte move dados; dbt transforma dados.**

O Airbyte será responsável pela camada de:

- Replicação
- Ingestion
- Sincronização entre source e destination

O dbt será responsável por:

- Limpeza
- Padronização
- Transformação
- Modelagem
- Testes

---

# 8. Airflow e pipeline operacional

## DAG principal

```text
DAG: football_data_pipeline

start
  ↓
trigger_airbyte
  ↓
wait_for_airbyte
  ↓
dbt_build
  ↓
dbt_test
  ↓
great_expectations
  ↓
publish_success / notify
```

## Conceitos que devem aparecer no projeto

- DAGs
- Tasks
- Dependencies
- Retries
- Timeouts
- Logging
- Failure handling
- Idempotency
- Scheduling
- Backfill

---

# 9. CI/CD e testes

| Check | Ferramenta | Objetivo |
|---|---|---|
| Pre-commit | pre-commit | Executar checks básicos antes do commit |
| Lint Python | Ruff | Qualidade e problemas de Python |
| Unit tests | Pytest | Testar loader e lógica Python |
| SQL lint | SQLFluff | Qualidade/formatação SQL |
| dbt parse | dbt | Validar projeto e dependências |
| dbt compile | dbt | Validar SQL compilado |
| dbt test | dbt | Integridade dos modelos |
| Data quality | Great Expectations | Regras de negócio e qualidade |
| IaC | Terraform | `fmt`, `validate`, `plan` |
| Security | Trivy + secret scan | Vulnerabilidades e credenciais expostas |

## Fluxo de CI

```text
checkout
  ↓
pre-commit
  ↓
Ruff
  ↓
Pytest
  ↓
SQLFluff
  ↓
dbt deps
  ↓
dbt parse
  ↓
dbt compile
  ↓
dbt test
  ↓
Terraform fmt
  ↓
Terraform validate
  ↓
Terraform plan
  ↓
Trivy / secret scan
  ↓
quality gate
  ↓
code review
  ↓
merge
```

---

# 10. Terraform

Terraform será usado como ferramenta de **Infrastructure as Code**.

O objetivo é declarar a infraestrutura/configuração que faz sentido, sem substituir Docker Compose indiscriminadamente.

## Estrutura sugerida

```text
terraform/
├── modules/
│   ├── postgres/
│   ├── airbyte/
│   └── monitoring/
├── environments/
│   ├── dev/
│   └── prod/
└── main.tf
```

## Validações no CI

```bash
terraform fmt -check
terraform init
terraform validate
terraform plan
```

Opcionalmente:

```text
tflint
security scan
```

## Possível uso com Airbyte

Considerar Terraform para declarar:

- Sources
- Destinations
- Connections

Para o runtime local, **Docker Compose continua sendo a ferramenta principal**.

Não é necessário forçar Terraform a substituir o Docker Compose.

---

# 11. Lineage e observabilidade

## Lineage

```text
Airflow
   ↓
OpenLineage
   ↓
Marquez
```

Exemplo:

```text
source.matches
      ↓
raw.matches
      ↓
stg_matches
      ↓
fct_match
      ↓
dashboard
```

## Métricas relevantes

- Pipeline success/failure
- Pipeline duration
- Rows ingested
- Rows rejected
- Freshness
- Duplicate rate
- NULL rate
- Data quality status

---

# 12. Metabase — produto final

Dashboard sugerido:

# Football Analytics

## KPIs

- Total de partidas
- Total de gols
- Média de gols por partida
- Percentual de vitórias em casa
- Percentual de empates
- Percentual de vitórias fora

## Análises

- Ranking por temporada
- Gols por temporada
- Performance de times ao longo do tempo
- Home advantage
- Head-to-head
- Sequências de vitórias
- Sequências sem derrotas

O objetivo do Metabase é demonstrar que o pipeline gera um produto analítico final, e não apenas tabelas técnicas.

---

# 13. Roadmap de implementação

## STEP 0 — Definir escopo

Fixar:

- Premier League como primeira competição
- Período inicial
- Métricas do dashboard

## STEP 1 — Criar GitHub repo

Criar:

- README
- `.gitignore`
- Licença
- Convenções
- Estrutura inicial

## STEP 2 — Docker base

Subir:

- PostgreSQL SOURCE
- PostgreSQL DW

Usando Docker Compose.

## STEP 3 — Dataset loader

Criar um loader Python para:

- Baixar/ler CSVs
- Processar os arquivos
- Carregar no SOURCE DB

## STEP 4 — Airbyte

Subir/configurar Airbyte.

Criar conexão:

```text
PostgreSQL SOURCE
        ↓
     Airbyte
        ↓
PostgreSQL DW.raw
```

## STEP 5 — dbt

Configurar:

- Projeto dbt
- Dependências
- Conexão com o DW

## STEP 6 — Staging

Criar modelos de staging com:

- Tipos
- Padronização de nomes
- Normalização
- Limpeza inicial

## STEP 7 — Intermediate

Criar:

- Lógica intermediária
- Enriquecimentos
- Transformações reutilizáveis

## STEP 8 — Marts

Criar:

- `fct_match`
- `fct_team_season`
- Métricas analíticas

## STEP 9 — dbt tests

Adicionar:

- `unique`
- `not_null`
- `relationships`
- `accepted_values`
- Testes customizados

## STEP 10 — Metabase

Criar o dashboard.

Validar que o produto final responde perguntas reais.

## STEP 11 — Airflow

Orquestrar:

```text
Airbyte
  ↓
dbt
  ↓
tests
  ↓
Data Quality
```

## STEP 12 — Great Expectations

Adicionar validações de:

- Volume
- Freshness
- Ranges
- Regras de negócio

## STEP 13 — Terraform

Declarar infraestrutura/configuração relevante e integrar validações ao CI.

## STEP 14 — GitHub Actions

Implementar CI completo:

- Lint
- Unit tests
- SQL tests
- dbt
- Terraform
- Security

## STEP 15 — Security

Adicionar:

- Trivy
- Secret scanning
- Revisão de permissões
- Revisão de secrets

## STEP 16 — CD

Automatizar deployment conforme a estratégia definida.

## STEP 17 — Lineage

Adicionar:

- OpenLineage
- Marquez

## STEP 18 — Observability

Adicionar:

- Métricas
- Logs
- Freshness
- Alertas básicos

## STEP 19 — Expandir domínio

Adicionar:

- Outras ligas
- Outras competições
- Segunda fonte, como OpenFootball

## STEP 20 — Versão AWS

Mapear componentes locais para AWS e implementar a segunda versão cloud.

---

# 14. Estrutura sugerida do repositório

```text
football-data-platform/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── terraform.yml
├── airflow/
│   ├── dags/
│   └── requirements.txt
├── airbyte/
│   └── connections/
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── tests/
│   ├── macros/
│   ├── seeds/
│   └── dbt_project.yml
├── ingestion/
│   ├── src/
│   └── tests/
├── data_quality/
│   └── expectations/
├── terraform/
│   ├── modules/
│   └── environments/
├── docker/
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── .pre-commit-config.yaml
├── .sqlfluff
├── README.md
└── architecture.png
```

---

# 15. Princípios técnicos que precisam aparecer no projeto

## Idempotência

Executar novamente não deve criar duplicação ou estado inconsistente.

## Incremental loading

Quando fizer sentido, evitar processar toda a história a cada execução.

## Data contracts

O schema esperado deve ser explícito.

## Schema evolution

Alterações de schema precisam ser detectadas e tratadas.

## Backfill

Permitir reprocessar uma temporada ou período.

## Separation of concerns

Responsabilidades:

```text
Airbyte → move dados
Airflow → orquestra
dbt → transforma
Data Quality → valida
Metabase → consome/visualiza
```

## Reprodutibilidade

Usar:

- Docker
- IaC
- Versionamento

## Security

Nunca versionar secrets.

## Observability

Ser capaz de saber:

- Se o pipeline rodou
- Se falhou
- Quanto tempo demorou
- Quantos dados processou
- Se os dados estão saudáveis

---

# 16. O que evitar no início

- Não começar com Kubernetes/EKS
- Não adicionar várias ligas/fontes antes de o pipeline Premier League funcionar
- Não usar Terraform apenas por obrigação
- Não duplicar a mesma validação em várias ferramentas sem motivo
- Não colocar transformação pesada no Airbyte
- Não começar pela AWS

## Estratégia

Primeiro:

```text
MVP local funcional
```

Depois:

```text
Production-like
```

Por fim:

```text
AWS / cloud version
```

---

# 17. Critérios de conclusão

O projeto estará em um estado muito bom quando:

- [ ] O ambiente local sobe via Docker
- [ ] O dataset Premier League é carregado no PostgreSQL SOURCE
- [ ] O Airbyte replica os dados para `raw`
- [ ] O Airflow executa o pipeline completo
- [ ] O dbt constrói `staging`, `intermediate` e `marts`
- [ ] Data Quality detecta violações de regras de negócio
- [ ] O Metabase mostra um dashboard funcional
- [ ] GitHub Actions bloqueia PRs com falhas
- [ ] Terraform valida/reproduz a infraestrutura definida
- [ ] O lineage pode ser visualizado
- [ ] O README permite que outra pessoa execute o projeto
- [ ] Existe documentação de decisões, trade-offs e troubleshooting

---

# 18. Contexto para continuar em novo chat

## Prompt de continuidade

> Quero continuar meu projeto Football Data Platform. É um projeto end-to-end de Data Engineering, inicialmente 100% local/open source, usando Football-Data.co.uk/Premier League como dataset principal. A stack é Docker, GitHub, Airbyte, PostgreSQL source + PostgreSQL DW, dbt, Airflow, Great Expectations, Terraform, GitHub Actions, Ruff, Pytest, SQLFluff, Trivy, OpenLineage/Marquez e Metabase. O documento de contexto define a arquitetura, modelo dimensional, testes e roadmap. Quero continuar pelo STEP X.

## Estratégia de evolução

```text
Primeiro MVP funcional
        ↓
Production-like
        ↓
Expandir para outras ligas/fontes
        ↓
Implementação AWS
```

---

# 19. Visão final do projeto

```text
                         FOOTBALL DATA PLATFORM

Football-Data.co.uk / OpenFootball
              ↓
      PostgreSQL SOURCE
              ↓
           Airbyte
              ↓
       PostgreSQL RAW
              ↓
             dbt
              ↓
     staging → intermediate → marts
              ↓
     ┌────────┴─────────┐
     ▼                  ▼
Data Quality        Metabase
     ▲
     │
  Airflow
     │
     └── orchestration

GitHub → GitHub Actions → CI/CD
Terraform → IaC
OpenLineage → Lineage
Trivy → Security
Docker → Reproducibility
```

---

# Resumo executivo

## Nome do projeto

**Football Data Platform**

## Dataset inicial

**Premier League — Football-Data.co.uk**

## Objetivo

Construir uma plataforma de dados end-to-end que demonstre competências modernas de Data Engineering.

## Fluxo principal

```text
Dataset
  ↓
Python Loader
  ↓
PostgreSQL Source
  ↓
Airbyte
  ↓
PostgreSQL DW / Raw
  ↓
dbt
  ↓
Data Quality
  ↓
Metabase
```

## Orquestração

```text
Airflow
```

## CI/CD

```text
GitHub + GitHub Actions
```

## IaC

```text
Terraform
```

## Qualidade

```text
Pytest
Ruff
SQLFluff
dbt tests
Great Expectations
```

## Segurança

```text
Trivy
Secret scanning
```

## Lineage

```text
OpenLineage + Marquez
```

## Evolução

```text
Local MVP
  ↓
Production-like
  ↓
Multiple sources / leagues
  ↓
AWS
```

---

> **Regra de continuidade do projeto:** construir primeiro o MVP funcional e adicionar complexidade de forma incremental. Não antecipar ferramentas ou arquitetura antes de haver necessidade real.
