# Football Data Platform — Project Progress

## Estado Atual

**STEP:** 1 — Criar estrutura base do repositório

**Última implementação concluída:** Estrutura inicial de pastas e documentação criada

**Status:** Estrutura de pastas criada localmente. Repositório GitHub ainda não criado.

**Próximo objetivo:** Criar o repositório no GitHub, inicializar Git, fazer primeiro commit.

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
| STEP 1 | Criar estrutura base / GitHub repo | 🔄 Em progresso |
| STEP 2 | Docker base (PostgreSQL SOURCE + DW) | ⬜ Pendente |
| STEP 3 | Dataset loader (Python) | ⬜ Pendente |
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
| PostgreSQL SOURCE | ⬜ Pendente | Será criado no STEP 2 |
| PostgreSQL DW | ⬜ Pendente | Será criado no STEP 2 |
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

## Próximos Passos

1. Criar repositório no GitHub: `football-data-platform`
2. Inicializar Git no diretório local
3. Fazer primeiro commit com estrutura base
4. Configurar branch protection no GitHub
