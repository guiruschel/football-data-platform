# Football Data Platform — Checklist

## Programas necessários

| Programa | Versão Mínima | Status | Observação |
|----------|--------------|--------|------------|
| Git | 2.x | ⬜ Verificar | Necessário para versionamento |
| Docker Desktop | 4.x | ⬜ Verificar | Runtime principal dos containers |
| Python | 3.11+ | ⬜ Verificar | Loader e scripts |
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
| Docker funcionando | ⬜ Verificar | `docker ps` sem erro |
| Python funcionando | ⬜ Verificar | `python --version` |
| Terraform funcionando | ⬜ Verificar | `terraform version` |
| Diretório do projeto criado | ✅ Concluído | `Football Data Platform/` |

---

## Repositório GitHub

| Item | Status | Observação |
|------|--------|------------|
| Repositório criado no GitHub | ⬜ Pendente | Nome sugerido: `football-data-platform` |
| Git inicializado localmente | ⬜ Pendente | `git init` |
| Remote configurado | ⬜ Pendente | `git remote add origin ...` |
| Primeiro commit realizado | ⬜ Pendente | Estrutura base |
| Branch `main` protegida | ⬜ Pendente | Exige PR para merge |
| Branch `develop` criada | ⬜ Pendente | Branch de desenvolvimento |

---

## Infraestrutura Docker

| Serviço | Status | Porta | Observação |
|---------|--------|-------|------------|
| PostgreSQL SOURCE | ⬜ Pendente | 5433 | Banco de origem dos dados |
| PostgreSQL DW | ⬜ Pendente | 5432 | Data Warehouse |
| Airbyte | ⬜ Pendente | 8000 | Interface web + API |
| Airflow | ⬜ Pendente | 8080 | Interface web |
| Metabase | ⬜ Pendente | 3000 | BI / Dashboards |
| Marquez | ⬜ Pendente | 5000 | Data lineage |

---

## Python / Projeto

| Item | Status | Observação |
|------|--------|------------|
| `pyproject.toml` criado | ✅ Concluído | Configuração do projeto Python |
| Ambiente virtual criado | ⬜ Pendente | `.venv/` no diretório do projeto |
| Dependências instaladas | ⬜ Pendente | `pip install -e ".[dev]"` |
| `pre-commit` instalado | ⬜ Pendente | `pre-commit install` |

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
| `.env.example` criado | ⬜ Pendente | Template de variáveis de ambiente |
| Trivy configurado | ⬜ Pendente | STEP 15 |
| Secret scanning ativo | ⬜ Pendente | STEP 15 |
