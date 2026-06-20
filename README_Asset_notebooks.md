# Summit 2026: Build an AI-Powered Enterprise Application

_Icons used throughout this lab: 🛠️ Action  📌 Note  🔹 Info_

> **Lab Code:** Elective E1 — End-to-End AI  
> **Lab Version:** FY27 Summit 2026 | **Last Updated:** May 21, 2026  
> ⏱️ **Timing Guidance:** ~3.0–3.5 hours end-to-end (Modules 01–08)
>
> 📌 **Naming Update (Summit 2026):** Snowflake Intelligence is now **CoWork**. Cortex Code is now officially **CoCo**. This lab uses the original names in some places — the product capabilities are identical.

### ▶️ Lab Overview Video

🎥 <a href="https://drive.google.com/file/d/1aaynDjTXN7zpSNbIX-h_kvfy6NVoS18F/view?usp=sharing" target="_blank">Watch the 1min overview video</a> — a quick walkthrough of what you'll build across all 9 modules.

---

## 🚀 Customer Workshop Version Available

A streamlined, customer-ready version of this HOL is now available in [customer_workshop/](../E2E_AI_HOL/customer_workshop/README.md)

This version consolidates the end-to-end flow into a single notebook designed for customer workshops, partner enablement, and field demos. It removes Summit-specific and internal-only content, uses customer-safe naming conventions (`AI_WORKSHOP_*`), and simplifies the experience with a guided workflow and optional industry-specific sample data customization.
 
---

## 🎯 Scenario: Nexus Capital

**Nexus Capital** is a financial data and analytics firm that processes:
- Real-time transactions (trades, client activity, portfolio positions)
- Analytical datasets (AUM, revenue by segment, risk metrics)
- Unstructured documents (research notes, compliance reports, market commentary)

Their challenge: AI tools can't access their data safely, don't understand business definitions, and can't take action across enterprise tools.

**In this lab, you'll build a Snowflake-native AI application layer** where AI understands analytics (OLAP), business meaning (semantic layer), and can investigate anomalies, answer business questions, and take action in enterprise systems — all within Snowflake's governed environment.

---

## 📋 Prerequisites

✅ **Snowflake Account Access**
- ACCOUNTADMIN privileges (for bootstrap)
- Ability to create Agents, Semantic Views, Cortex Search Services, and MCP Servers
- Cross-region inference enabled (or ability to enable it)

✅ **Recommended Background**
- Familiarity with Snowflake SQL fundamentals
- Basic understanding of CoWork (formerly Snowflake Intelligence) ([L100 Course](https://scout.snowflake.com/learn/courses/49927/l100-snowflake-intelligence))

✅ **For Optional Modules**
- Snowflake Postgres enabled on account (Module 09)
- Atlassian account — free tier works (Module 05)
- Personal Gmail account (Module 05 — optional Google connectors)

---

## ▶️ Lab Modules

### Core (Required)

| # | Module | What You'll Build | Time |
|---|--------|-------------------|------|
| [01](./notebooks/Notebook_01_HOL_Setup.ipynb) | **HOL Setup** | Database, schemas, warehouse, roles, grants + gold-layer analytics data | 15–20 min |
| [02](./notebooks/Notebook_02_Semantic_Layer.ipynb) | **Semantic Layer** | Semantic view (dimensions, metrics, verified queries) + Cortex Search service | 25–30 min |
| [03](./notebooks/Notebook_03_Cortex_Agent.ipynb) | **Cortex Agent (API)** | Agent wired to semantic view + search, tested via SQL and REST API. Includes optional Agent Evaluations, AI Observability, and CoCo-powered improvement workflow. | 25–30 min |
| [04](./notebooks/Notebook_04_CoWork.ipynb) | **CoWork** | SI chat deployment, SI-only role, artifacts, monitoring, customization | 20–25 min |
| [05](./notebooks/Notebook_05_MCP_Connectors.ipynb) | **MCP Connectors** | Atlassian (Jira/Confluence) + optional Google/Slack | 20–25 min |
| [06](./notebooks/Notebook_06_AI_Security.ipynb) | **AI Security & Governance** | RBAC, Guardrails, PII Redaction, trust boundary, audit trail | 15–20 min |
| [07](./notebooks/Notebook_07_CoCo.ipynb) | **CoCo** | Debug inefficient queries, validate agent, build Custom AI Function | 20–25 min |
| [08](./notebooks/Notebook_08_Validation.ipynb) | **End-to-End Validation** | Full scenario test + DORA completion check (SL1_01) | 10–15 min |

> **Total Core: ~2.5–3.5 hours**

### Optional Extension

| # | Module | What You'll Build | Time |
|---|--------|-------------------|------|
| [09](./notebooks/Notebook_09_Postgres_Transactional.ipynb) | **Transactional Layer** | Snowflake Postgres instance + market index data + live order flow + agent queries transactional data | 15–20 min |

---

## 🏗️ Naming Conventions

| Object Type | Name | Notes |
|---|---|---|
| **Database** | `NEXUS_HOL` | All lab assets live here |
| **Schemas** | `ANALYTICS`, `SEMANTIC`, `AGENTS`, `TRANSACTIONS` | Maps to lab progression |
| **Warehouse** | `NEXUS_WH` | XS, auto-suspend 60s |
| **Role** | `NEXUS_ADMIN` | Full lab privileges |
| **SI Role** | `NEXUS_SI_USER` | Business user scoped access |
| **Agent** | `NEXUS_AGENT` | The enterprise AI agent |
| **Semantic View** | `NEXUS_CAPITAL_SV` | Business metrics definition |
| **Search Service** | `NEXUS_RESEARCH_SEARCH` | RAG over research notes |
| **MCP Server** | `NEXUS_ATLASSIAN_MCP` | Jira/Confluence connector |
| **Custom Function** | `CLASSIFY_TRADE_CONVICTION` | Trade note classifier |

---

## 🧠 The Story Arc

```
Gold-Layer Analytics (Module 01)
    → Semantic Layer (Module 02)
        → Cortex Agent API (Module 03)
            → CoWork (Module 04)
                → MCP Connectors (Module 05)
                    → AI Security (Module 06)
                        → CoCo + Custom AI Functions (Module 07)
                            → End-to-End Validation (Module 08)

Optional: Postgres + Transactional Data (Module 09)
```

---

## 🔑 Fill-in-the-Blank (XXX) Replacement Guide

Throughout this lab, critical code sections contain `XXX` placeholders. You must fill these in to proceed — they force understanding of key connection points.

### Module 02: Semantic Layer

| # | Location | Replace XXX With | Why |
|---|----------|-----------------|-----|
| 1 | `RELATIONSHIPS` clause — `positions(XXX)` and `trades(XXX)` | `CLIENT_ID` | This is the foreign key that joins positions and trades to the clients table. Defined as the PRIMARY KEY on clients. |
| 2 | Verified query `WHERE STATUS = 'XXX'` | `ACTIVE` | We only want current clients in "top clients" results. STATUS can be ACTIVE or INACTIVE. |
| 3 | `CREATE CORTEX SEARCH SERVICE ... ON XXX` | `CONTENT` | The `ON` clause specifies which column contains the main text to index. CONTENT holds the body of each research note. |

### Module 03: Cortex Agent

| # | Location | Replace XXX With | Why |
|---|----------|-----------------|-----|
| 1 | `tool_resources` → `semantic_view:` | `NEXUS_HOL.SEMANTIC.NEXUS_CAPITAL_SV` | Connects the Cortex Analyst tool to the semantic view. Must be fully qualified (DB.SCHEMA.NAME). |
| 2 | `execution_environment` → `warehouse:` | `NEXUS_WH` | The XS warehouse the agent uses to execute generated SQL. Agents are serverless and don't inherit session warehouse. |

### Module 05: MCP Connectors

| # | Location | Replace XXX With | Why |
|---|----------|-----------------|-----|
| 1 | `CREATE EXTERNAL MCP SERVER` → `URL =` | `https://mcp.atlassian.com/v1/mcp` | Atlassian's MCP endpoint. Matches the `OAUTH_RESOURCE_URL` in the API Integration above. |

### Module 06: AI Security & Governance

| # | Location | Replace XXX With | Why |
|---|----------|-----------------|-----|
| 1 | `ALTER ACCOUNT SET AI_SETTINGS` → guardrail type | `advanced_prompt_injection` | The specific guardrail that detects and blocks adversarial prompts attempting to override system instructions. |
| 2 | `AI_REDACT(EMAIL, ['XXX'])` → PII category | `EMAIL` | The category tells AI_REDACT what pattern to detect and replace with `[EMAIL]`. |

### Module 07: CoCo

| # | Location | Replace XXX With | Why |
|---|----------|-----------------|-----|
| 1 | `SNOWFLAKE.CORTEX.COMPLETE('XXX', ...)` in CLASSIFY_TRADE_CONVICTION | `claude-haiku-4-5` | For a simple classification task, a smaller/faster model reduces cost without sacrificing quality. This is the cost-quality tradeoff that Custom AI Functions automate. |

---

## 🗣️ Field Talking Points

- "In 3 hours, I built a production-ready AI application — from semantic layer to governed agent to enterprise automation."
- "Same agent, three delivery channels: REST API for developers, CoWork (formerly Snowflake Intelligence) for business users, MCP for enterprise tools."
- "Governance isn't bolted on — it's built in. RBAC, PII masking, guardrails, credit budgets, and full audit trail from day one."
- "The semantic view is the single source of truth for AI understanding. Build it once, every tool gets consistent answers."
- "MCP transforms agents from answering machines into action-takers — create Jira tickets, search Gmail, post to Slack."
- "Custom AI Functions close the gap between AI experimentation and production — optimized, governed, reusable."

---

## 📚 Key References

| Resource | Link |
|----------|------|
| CoWork (formerly Snowflake Intelligence) | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence) |
| Cortex Agents | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) |
| Semantic Views | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/semantic-view) |
| MCP Connectors | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp-connectors) |
| CoCo | [Documentation](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) |
| Cross-region Inference | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) |
| AI_REDACT | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/redact-pii) |
| Cortex AI Guardrails | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-guardrails) |
| SI GA HOL (full L200, 13 modules) | [GitHub](https://github.com/snowflake-corp/collegeai/blob/initial-import/SI_GA_HOL/README.md) |
| Ontology on Snowflake | [Scout](https://scout.snowflake.com/learn/courses/50217/ontology-on-snowflake-enabling-business-aware-ai) |
| Global vs Regional AI Inference (video) | [Seismic](https://snowflake.seismic.com/Link/Content/DCpXdpMXW43Bj82MdqCbhQJq9ghG) |
| AI Pricing FAQ | [GDoc](https://docs.google.com/document/d/10k7wZLUN3tybElajcKuSccplCaYx4xEmx70HovXbVrw/edit) |
| Agent Evaluations | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-evaluations) |
| AI Observability | [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability) |

---

## 📂 File Structure

```
E2E_AI_HOL/
├── README.md                    ← You are here
├── notebooks/
│   ├── Notebook_01_HOL_Setup.ipynb
│   ├── Notebook_02_Semantic_Layer.ipynb
│   ├── Notebook_03_Cortex_Agent.ipynb
│   ├── Notebook_04_CoWork.ipynb
│   ├── Notebook_05_MCP_Connectors.ipynb
│   ├── Notebook_06_AI_Security.ipynb
│   ├── Notebook_07_CoCo.ipynb
│   ├── Notebook_08_Validation.ipynb
│   └── Notebook_09_Postgres_Transactional.ipynb  (optional)
├── assets/
│   └── call_nexus_agent.py      (REST API Python client)
├── customer_workshop/
│   ├── AI_Workshop_Customer.ipynb       ← Customer-ready single notebook workshop
│   └── README.md               ← Customer workshop guide and setup
```

---

## 🧹 Cleanup

```sql
-- Suspend warehouse (stops compute billing)
ALTER WAREHOUSE NEXUS_WH SUSPEND;

-- Drop Postgres instance if created (Module 09)
DROP POSTGRES INSTANCE IF EXISTS NEXUS_POSTGRES;

-- Full removal (optional):
DROP DATABASE IF EXISTS NEXUS_HOL;
DROP WAREHOUSE IF EXISTS NEXUS_WH;
DROP ROLE IF EXISTS NEXUS_ADMIN;
DROP ROLE IF EXISTS NEXUS_SI_USER;
```

> **Keep it?** If you plan to demo to customers, just suspend the warehouse. The database and agent cost nothing when idle.

---

**Questions?** Contact Diana Shaw or check the lab documentation.
