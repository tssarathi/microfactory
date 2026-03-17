# microfactory

Multi-agent field service operations platform for HVAC, electrical, plumbing, and refrigeration services across Brisbane metro (QLD, Australia).

## Overview

AI agents manage work orders, equipment, parts inventory, and technical knowledge for a fictional field service company. Built with Google ADK agents communicating through MCP tool servers, with a RAG knowledge base as standalone infrastructure — all running locally via Ollama.

Demonstrates the AI Factory approach: agentic teams, local data ownership, real business domain problems.

## Architecture

```
User
 └─► Field Service Agent (qwen3:8b via LiteLLM)
      └─► Database MCP Server ──► SQLite (9 tables, 222 records)

Knowledge Base MCP Server ──► ChromaDB (25 docs, cosine similarity)
   (not yet connected to an agent)        ▲
                                     nomic-embed-text
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.14 |
| Package manager | uv (workspace) |
| LLM runtime | Ollama |
| Agent framework | Google ADK |
| LLM routing | LiteLLM |
| Tool protocol | MCP via FastMCP |
| Vector database | ChromaDB (Docker) |
| Relational database | SQLite |
| Text splitting | LangChain text splitters |

## Project Structure

```
microfactory/
├── agents/
│   ├── field_service/    # Work orders, equipment, parts (qwen3:8b)
│   └── knowledge/        # Technical knowledge RAG (stub)
├── tools/
│   ├── database/         # FastMCP server → SQLite
│   └── knowledge_base/   # FastMCP server → ChromaDB
├── scripts/
│   ├── create_database.py
│   └── create_vectors.py
├── data/
│   ├── bronze/           # Raw CSVs + knowledge markdown
│   └── silver/           # SQLite DB + vector store
├── docs/                 # Capability matrix, data schema, roadmap
└── docker-compose.yml    # ChromaDB service
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Ollama](https://ollama.com/download): `curl -fsSL https://ollama.com/install.sh | sh`
- [Docker](https://docs.docker.com/get-docker/) (for ChromaDB)

## Setup

```bash
# Clone and enter the project
git clone https://github.com/sarathi/microfactory.git
cd microfactory

# Configure environment
cp .env.example .env

# Pull models
ollama pull qwen3:8b
ollama pull nomic-embed-text

# Install dependencies
uv sync --all-packages

# Start services (each in its own terminal)
ollama serve
docker compose up

# Seed the database
uv run python scripts/create_database.py

# Create vector embeddings
uv run python scripts/create_vectors.py
```

## What the Agent Can Do

The field service agent connects to the database MCP server and can:

- **Work orders** — search and view by status, priority, trade, or customer
- **Customers** — look up contact details and service history
- **Equipment** — check equipment records and maintenance history for a customer
- **Parts** — search inventory and check availability

## Data

9 tables and 222 seed records in SQLite, plus 25 technical knowledge documents in ChromaDB.
Covers customers, technicians, equipment, work orders, parts inventory, schedules, and job notes across Brisbane metro service areas.

See [data/README.md](data/README.md) for the full schema reference and knowledge base document list.

---

Thank you for visiting and checking out microfactory!
