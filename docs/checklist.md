# Football Data Platform — Checklist

## Programas necessários

| Programa | Versão Mínima | Status | Observação |
|----------|--------------|--------|------------|
| Git | 2.x | ⬜ Verificar | Necessário para versionamento |
| Docker Desktop | 4.x | ✅ Concluído | Runtime principal dos containers |
| Python | 3.11+ | ⬜ Opcional | Só necessário se você quiser rodar fora do Docker |
| VS Code | Qualquer | ⬜ Verificar | Editor |
| Terraform | 1.6+ | ⬜ Verificar | IaC |
| GitHub CLI (gh) | Opcional | ⬜ Verificar | Facilita operações GitHub |
| PostgreSQL Client (psql) | Qualquer | ⬜ Verificar | Acesso local ao banco |
| dbt Core | 1.7+ | ⬜ Pendente | Instalado via pip no projeto |
| Ruff | Qualquer | ⬜ Pendente | Instalado via pip no projeto |
| SQLFluff | Qualquer | ⬜ Pendente | Instalado via pip no projeto |
| pre-commit | Qualquer | ⬜ Pendente | Instalado via pip no projeto |

---

## Contas e Acessos

| Conta/Acesso | Status | Observação |
|-------------|--------|------------|
| GitHub (conta pessoal) | ⬜ Verificar | Necessário para repositório e CI/CD |
| Docker Hub | ⬜ Verificar | Necessário para imagens Docker |
| Football-Data.co.uk | ⬜ Verificar | Dataset principal (gratuito, sem cadastro obrigatório para CSV histórico) |

---

## Configuração do Ambiente

| Item | Status | Observação |
|------|--------|------------|
| Git configurado (nome + email) | ⬜ Verificar | `git config --global` |
| GitHub SSH configurado | ⬜ Verificar | Chave SSH adicionada ao GitHub |
| Docker funcionando | ✅ Concluído | `docker version` e `docker compose up -d` sem erro |
| Docker Desktop instalado neste notebook | ✅ Concluído | Sem impactar o ambiente do trabalho |
| Python no host funcionando | ⬜ Opcional | O projeto roda dentro do Docker |
| Terraform funcionando | ⬜ Verificar | `terraform version` |
| Diretório do projeto criado | ✅ Concluído | `Football Data Platform/` |
| Virtualenv do projeto criada | ⬜ Pendente | `.venv/` local do projeto |

---

## Repositório GitHub

| Item | Status | Observação |
|------|--------|------------|
| Repositório criado no GitHub | ✅ Concluído | `football-data-platform` |
| Git inicializado localmente | ✅ Concluído | `git init` |
| Remote configurado | ✅ Concluído | `git remote add origin ...` |
| Primeiro commit realizado | ✅ Concluído | Estrutura base |
| Branch `main` protegida | ⬜ Pendente | Exige PR para merge |
| Branch `develop` criada | ⬜ Pendente | Branch de desenvolvimento |

---

## Infraestrutura Docker

| Serviço | Status | Porta | Observação |
|---------|--------|-------|------------|
| PostgreSQL SOURCE | ✅ Concluído | 5435 | Banco de origem dos dados |
| PostgreSQL DW | ✅ Concluído | 5434 | Data Warehouse |
| Airbyte | ⬜ Pendente | 8000 | Interface web + API |
| Airflow | ⬜ Pendente | 8080 | Interface web |
| Metabase | ⬜ Pendente | 3000 | BI / Dashboards |
| Marquez | ⬜ Pendente | 5000 | Data lineage |

---

## Python / Projeto

| Item | Status | Observação |
|------|--------|------------|
| `pyproject.toml` criado | ✅ Concluído | Configuração do projeto Python |
| Ambiente virtual criado | ⬜ Não necessário | O loader roda em container |
| Dependências instaladas | ✅ Concluído | Instaladas na imagem Docker do loader |
| `pre-commit` instalado | ⬜ Pendente | Opcional enquanto o fluxo Docker estiver consolidado |
| `.env` local criado | ✅ Concluído | Somente neste notebook, fora do Git |
| Loader Python em Docker | ✅ Concluído | Serviço `ingestion` no `docker-compose.yml` |
| Testes do loader em Docker | ✅ Concluído | `pytest` passou no container |
| Loader carregou `raw_matches` | ✅ Concluído | `13321` linhas no `football_source.raw_matches` |

---

## dbt

| Item | Status | Observação |
|------|--------|------------|
| Projeto dbt inicializado | ⬜ Pendente | `dbt/` |
| Conexão com DW configurada | ⬜ Pendente | `profiles.yml` |
| Modelos staging criados | ⬜ Pendente | STEP 6 |
| Modelos intermediate criados | ⬜ Pendente | STEP 7 |
| Modelos marts criados | ⬜ Pendente | STEP 8 |
| Testes dbt configurados | ⬜ Pendente | STEP 9 |

---

## CI/CD

| Item | Status | Observação |
|------|--------|------------|
| `ci.yml` criado | ⬜ Pendente | STEP 14 |
| `cd.yml` criado | ⬜ Pendente | STEP 16 |
| `terraform.yml` criado | ⬜ Pendente | STEP 13/14 |
| Secrets configurados no GitHub | ⬜ Pendente | STEP 14 |

---

## Data Quality

| Item | Status | Observação |
|------|--------|------------|
| dbt tests configurados | ⬜ Pendente | STEP 9 |
| Great Expectations configurado | ⬜ Pendente | STEP 12 |
| Expectativas criadas | ⬜ Pendente | STEP 12 |

---

## Segurança

| Item | Status | Observação |
|------|--------|------------|
| `.gitignore` configurado | ✅ Concluído | Secrets e arquivos sensíveis ignorados |
| `.env.example` criado | ✅ Concluído | Variáveis de ambiente específicas do projeto |
| Trivy configurado | ⬜ Pendente | STEP 15 |
| Secret scanning ativo | ⬜ Pendente | STEP 15 |
