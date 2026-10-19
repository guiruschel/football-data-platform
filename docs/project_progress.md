# Football Data Platform — Project Progress

## Estado Atual

**STEP:** 4 — Airbyte

**Última implementação concluída:** Loader Python executado e testado com sucesso dentro do Docker

**Status:** O loader e os testes já rodam dentro do container `ingestion`, sem depender do Python do Windows. O source recebeu carga inicial com sucesso.

**Próximo objetivo:** Subir e configurar o Airbyte para replicar `postgres_source` → `postgres_dw`.

---

## Histórico de Progresso

### [2026-08-22] — Início do projeto

**O que foi feito:**
- Definição de escopo: Premier League, Football-Data.co.uk, período 1993 → atual
- Documento de contexto principal criado: `docs/football_data_engineering_e2e_project_context.md`
- Estrutura de pastas do projeto criada localmente
- Arquivos base criados: `docs/project_progress.md`, `docs/checklist.md`
- `.gitignore` criado
- `README.md` criado com visão geral do projeto
- `Makefile` base criado
- `pyproject.toml` base criado
- `.pre-commit-config.yaml` base criado
- `.sqlfluff` base criado
- Base Docker isolada iniciada com `docker-compose.yml` e `.env.example`
- `.env` local criado para o Docker Compose do projeto
- Containers `postgres_source` e `postgres_dw` subidos com sucesso
- Conexões DBeaver validadas para `football_source` e `football_dw`
- Estrutura inicial do loader criada em `ingestion/src/football_data_platform`
- Testes unitários iniciais criados para helpers de URL e preparação de dados
- Serviço Docker `ingestion` criado para rodar Python e testes dentro do container
- `pytest` do loader passou dentro do Docker (`5 passed`)
- Loader executado com sucesso e carregou `13321` linhas em `football_source.raw_matches`

**Decisões técnicas:**
- Projeto 100% local/Docker na primeira fase
- Dataset inicial: Premier League, grão por partida
- Dois bancos PostgreSQL: SOURCE (dados originais) e DW (raw + staging + marts)
- Airbyte como ferramenta de replicação SOURCE → DW
- dbt para todas as transformações
- Airflow para orquestração

**Problemas encontrados:** Nenhum até o momento.

---

## Roadmap — Status

| STEP | Descrição | Status |
|------|-----------|--------|
| STEP 0 | Definir escopo | ✅ Concluído |
| STEP 1 | Criar estrutura base / GitHub repo | ✅ Concluído |
| STEP 2 | Docker base (PostgreSQL SOURCE + DW) | ✅ Concluído |
| STEP 3 | Dataset loader (Python) | ✅ Concluído |
| STEP 4 | Airbyte | ⬜ Pendente |
| STEP 5 | dbt — configuração inicial | ⬜ Pendente |
| STEP 6 | dbt — Staging | ⬜ Pendente |
| STEP 7 | dbt — Intermediate | ⬜ Pendente |
| STEP 8 | dbt — Marts | ⬜ Pendente |
| STEP 9 | dbt tests | ⬜ Pendente |
| STEP 10 | Metabase | ⬜ Pendente |
| STEP 11 | Airflow | ⬜ Pendente |
| STEP 12 | Great Expectations | ⬜ Pendente |
| STEP 13 | Terraform | ⬜ Pendente |
| STEP 14 | GitHub Actions (CI) | ⬜ Pendente |
| STEP 15 | Security (Trivy + secret scan) | ⬜ Pendente |
| STEP 16 | CD | ⬜ Pendente |
| STEP 17 | Lineage (OpenLineage + Marquez) | ⬜ Pendente |
| STEP 18 | Observability | ⬜ Pendente |
| STEP 19 | Expandir domínio | ⬜ Pendente |
| STEP 20 | Versão AWS | ⬜ Pendente |

---

## Infraestrutura

| Componente | Status | Observação |
|------------|--------|------------|
| PostgreSQL SOURCE | ✅ Concluído | Acessível localmente via porta 5435 |
| PostgreSQL DW | ✅ Concluído | Acessível localmente via porta 5434 |
| Airbyte | ⬜ Pendente | Será configurado no STEP 4 |
| Airflow | ⬜ Pendente | Será configurado no STEP 11 |
| Metabase | ⬜ Pendente | Será configurado no STEP 10 |
| Marquez | ⬜ Pendente | Será configurado no STEP 17 |

---

## Variáveis de Ambiente Necessárias

| Variável | Descrição | Status |
|----------|-----------|--------|
| `POSTGRES_SOURCE_HOST` | Host do banco SOURCE | ⬜ Pendente |
| `POSTGRES_SOURCE_PORT` | Porta do banco SOURCE | ⬜ Pendente |
| `POSTGRES_SOURCE_DB` | Nome do banco SOURCE | ⬜ Pendente |
| `POSTGRES_SOURCE_USER` | Usuário do banco SOURCE | ⬜ Pendente |
| `POSTGRES_SOURCE_PASSWORD` | Senha do banco SOURCE | ⬜ Pendente |
| `POSTGRES_DW_HOST` | Host do banco DW | ⬜ Pendente |
| `POSTGRES_DW_PORT` | Porta do banco DW | ⬜ Pendente |
| `POSTGRES_DW_DB` | Nome do banco DW | ⬜ Pendente |
| `POSTGRES_DW_USER` | Usuário do banco DW | ⬜ Pendente |
| `POSTGRES_DW_PASSWORD` | Senha do banco DW | ⬜ Pendente |

---

## Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `docs/football_data_engineering_e2e_project_context.md` | Contexto técnico e estratégico do projeto |
| `docs/project_progress.md` | Estado operacional atual do projeto |
| `docs/checklist.md` | Checklist de programas, acessos e configurações |
| `docker-compose.yml` | Definição dos containers locais |
| `Makefile` | Comandos úteis do projeto |
| `pyproject.toml` | Configuração Python do projeto |
| `.pre-commit-config.yaml` | Hooks de pre-commit |
| `.sqlfluff` | Configuração do SQLFluff |

---

## Decisões Arquiteturais

| Decisão | Justificativa |
|---------|---------------|
| Dois bancos PostgreSQL (SOURCE + DW) | Simula ambiente real com sistema de origem separado do DW |
| Airbyte para replicação SOURCE → DW | Demonstra uso de ferramenta de ingestion padrão de mercado |
| dbt para todas as transformações | Separação clara de responsabilidades: Airbyte move, dbt transforma |
| Docker Compose como runtime local | Ambiente reproduzível sem dependência de cloud |
| Terraform para IaC declarativo | Configuração de infra reproduzível e versionada |

---

## BI Focus Areas

These are the first analysis themes planned for the BI layer:

1. **Team performance**
	- wins, draws, losses
	- goals scored and conceded
	- goal difference
	- points by season
	- ranking over time

2. **Recent form and consistency**
	- last 5 or 10 matches by team
	- winning and losing streaks
	- unbeaten runs

3. **Season-to-season comparison**
	- team performance changes over the years
	- teams that improved or declined in level
	- evolution of home wins, draws, and losses
	- comparison of points and goal difference across seasons

---

## Próximos Passos

1. Subir e configurar o Airbyte local
2. Criar a conexão `postgres_source` → `postgres_dw`
3. Validar o primeiro sync para a camada `raw`
4. Depois seguir para o STEP 5 com dbt
