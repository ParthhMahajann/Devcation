# 🧠 Arogya AI

> **A Medical Knowledge Graph Platform** — AI-powered symptom diagnosis, drug interaction detection, and patient risk assessment using TigerGraph.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Built With](https://img.shields.io/badge/built%20with-React%20%7C%20FastAPI%20%7C%20TigerGraph-green)
![Hackathon](https://img.shields.io/badge/hackathon-Devcation-purple)

---

## 🚀 What is Arogya AI?

Arogya AI is a full-stack medical intelligence platform built on top of a **graph database**. It models the complex relationships between diseases, symptoms, drugs, genes, side effects, and patients — then lets you query those relationships in real time.

Instead of flat tables, we use **graph traversal** to answer questions like:
- *"A patient has fever, fatigue, and chest pain — what diseases match?"*
- *"Are these 4 medications safe to take together?"*
- *"What is this patient's overall drug interaction risk score?"*

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Symptom Checker** | Input multiple symptoms → get ranked differential diagnoses with confidence scores |
| 💊 **Drug Interaction Detector** | Input a medication list → visualize dangerous interaction networks |
| 🧬 **Patient Risk Profiler** | View a patient's full risk assessment based on their conditions and medications |
| 🌐 **Graph Explorer** | Interactively explore the entire medical knowledge graph |
| 📊 **Dashboard** | High-level stats on the graph — vertex/edge counts, query metrics |

---

## 🏗️ Architecture

```
[React Frontend]  ←── HTTP/REST ──→  [FastAPI Backend]  ←── pyTigerGraph ──→  [TigerGraph DB]
     :5173                                :8000                                  :9000 / :14240
```

The system is composed of three layers:

**Frontend** — React + Vite + Tailwind CSS, with `react-force-graph-2d` for interactive graph visualization.

**Backend** — FastAPI serving REST endpoints for diagnosis, drug interaction checking, patient risk, and graph exploration. Communicates with TigerGraph via `pyTigerGraph`.

**Database** — TigerGraph stores the medical knowledge graph (diseases, symptoms, drugs, genes, patients) and runs optimized GSQL queries including multi-hop traversal, shortest path, PageRank, and community detection.

---

## 🗂️ Graph Schema

### Vertices

| Vertex | Key Attributes |
|---|---|
| `Disease` | name, icd_code, severity, category |
| `Symptom` | name, body_system, severity_weight |
| `Drug` | name, drug_class, approval_status |
| `SideEffect` | name, severity |
| `Gene` | name, chromosome, function_desc |
| `Patient` | age, gender, blood_type |

### Edges

| Edge | From → To | Attributes |
|---|---|---|
| `HAS_SYMPTOM` | Disease ↔ Symptom | frequency, weight |
| `TREATS` | Drug → Disease | efficacy_score, evidence_level |
| `CAUSES_SIDE_EFFECT` | Drug → SideEffect | probability |
| `INTERACTS_WITH` | Drug ↔ Drug | interaction_type, severity |
| `TARGETS_GENE` | Drug → Gene | mechanism |
| `ASSOCIATED_WITH` | Gene → Disease | evidence_strength |
| `DIAGNOSED_WITH` | Patient → Disease | diagnosis_date, status |
| `TAKES_DRUG` | Patient → Drug | dosage, start_date |
| `SYMPTOM_OVERLAP` | Symptom ↔ Symptom | correlation_score |

---

## 🔎 GSQL Queries

The core intelligence lives in four installed GSQL queries:

- **`diagnose_from_symptoms`** — Multi-hop weighted traversal from symptoms to diseases, scoring by edge weight × symptom severity
- **`check_drug_interactions`** — N-hop traversal across `INTERACTS_WITH` edges to find dangerous drug combinations
- **`find_treatment_path`** — Shortest path between a disease and a target drug
- **`patient_risk_profile`** — Aggregates interaction severity and gene-disease associations for a given patient

Plus TigerGraph built-in algorithms: **PageRank** (disease centrality) and **Community Detection** (symptom clustering).

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/symptoms/diagnose` | Symptoms → ranked diagnoses |
| `GET` | `/api/symptoms/list` | All symptoms (for autocomplete) |
| `POST` | `/api/drugs/interactions` | Drug list → interaction network |
| `GET` | `/api/drugs/list` | All drugs |
| `GET` | `/api/drugs/{id}` | Drug details + side effects |
| `GET` | `/api/patients/{id}/risk` | Patient risk profile |
| `POST` | `/api/patients` | Create/update patient |
| `GET` | `/api/graph/stats` | Graph statistics |
| `GET` | `/api/graph/explore` | Subgraph for visualization |

---

## 🧱 Project Structure

```
Devcation/
├── frontend/
│   └── src/
│       ├── pages/          # Dashboard, Diagnose, Interactions, Patient, Explore, About
│       ├── components/     # Reusable UI (GraphVisualization, SymptomInput, DrugSearch, ...)
│       ├── api/            # Axios clients per domain
│       └── hooks/          # useGraphData, useDiagnosis
├── ARCHITECTURE.md
├── TEAM_ROLES.md
├── TIMELINE.md
├── PROJECT_PLAN.md
└── PPT_STRUCTURE.md
```

---

## 🛠️ Tech Stack

**Frontend**
- React 18 + Vite
- Tailwind CSS
- react-force-graph-2d
- Axios
- react-router-dom
- Recharts
- react-select

**Backend**
- Python 3.11+
- FastAPI
- pyTigerGraph
- Pydantic
- Uvicorn

**Database**
- TigerGraph (GSQL, REST API, graph algorithms)

**Data Sources**
- DrugBank (drug interactions)
- SIDER (drug side effects)
- DisGeNET (gene–disease associations)
- Disease Ontology (ICD codes, disease hierarchy)
- Synthetic patient data (demo)

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Access to a TigerGraph instance (or Docker — see below)

### Quick Start with Docker

```bash
cp .env.example .env           # fill in TG credentials + MEDGRAPH_API_KEY
docker compose up -d           # starts TigerGraph + FastAPI
# wait ~90s for TigerGraph to initialise, then:
python tigergraph/setup.py     # create schema + install queries
python tigergraph/seed_data.py # load sample data
```

Frontend (separate terminal):
```bash
cd frontend && npm install
cp .env.example .env           # set VITE_API_URL and VITE_API_KEY
npm run dev                    # http://localhost:5173
```

### Manual Setup

#### Frontend

```bash
cd frontend
npm install
cp .env.example .env        # Set VITE_API_URL=http://localhost:8000
npm run dev                 # Runs on http://localhost:5173
```

#### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # Set TG_HOST, TG_USERNAME, TG_PASSWORD, TG_GRAPH, MEDGRAPH_API_KEY
uvicorn app.main:app --reload   # Runs on http://localhost:8000
```

#### TigerGraph

1. Create a graph named `MedGraph` on your TigerGraph instance
2. Run the GSQL schema creation scripts from `ARCHITECTURE.md`
3. Load CSV data from `data/processed/` using the provided loading jobs
4. Install the GSQL queries

---

## 🔐 Authentication

All API endpoints require an `X-API-Key` header.

**Set the key in `.env`:**
```
MEDGRAPH_API_KEY=your-secret-key-here
```

**Pass it in requests:**
```bash
curl -H "X-API-Key: your-secret-key-here" http://localhost:8000/api/graph/stats
```

The frontend reads the key from `VITE_API_KEY` in `frontend/.env` and sends it automatically.

> For local development the default key is `dev-insecure-key-change-me`. **Change this before any public deployment.**

---

## 🛠️ Troubleshooting

**TigerGraph won't connect**
- Check `TG_HOST`, `TG_USERNAME`, `TG_PASSWORD`, `TG_GRAPH` in `.env`
- Ensure the graph name matches exactly (default: `MedGraph`)
- Docker users: wait the full 90s start period before running setup scripts
- Check logs: `docker compose logs tigergraph`

**"Database unavailable" (503) on all API calls**
- TigerGraph is not running or the connection details are wrong
- For local development without TigerGraph, set `USE_MOCK_DATA=true` in `.env` to use demo data

**Frontend shows "Cannot reach the server"**
- Verify the backend is running on port 8000
- Check `VITE_API_URL` in `frontend/.env` matches the backend address
- Ensure `VITE_API_KEY` matches `MEDGRAPH_API_KEY` in the backend `.env`

**Rate limit errors (429)**
- Sensitive endpoints allow 30 req/min; list endpoints allow 60 req/min
- If you hit limits during development, wait 60 seconds or restart the backend

---

## 📊 Data Scale

The graph is designed to handle:

- 5,000+ diseases
- 10,000+ symptoms
- 3,000+ drugs
- 500+ genes
- 50,000+ edges
- 100 synthetic patients (for demo)

---

## 👥 Team

Built for **Devcation** hackathon by the **Arogya AI Team**.

| Name | Role | Responsibilities |
|---|---|---|
| **Manish Srivastav** |  Team Lead | Pydantic models, Swagger docs, pyTigerGraph integration|
| **Parth Mahajan** | Graph Engineer / Backend API Developer | TigerGraph schema, FastAPI endpoints, GSQL queries, pyTigerGraph integration |
| **Aakash Sarang** | Frontend Developer | React UI, graph visualization, dashboard, UX |
| **Krishiv Sharma** | Data + Presentation Lead | Data sourcing/cleaning, PPT, demo video, documentation |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> ⚠️ **Disclaimer:** Arogya AI is a research and demonstration tool built for a hackathon. It is **not** intended for real clinical use. Always consult a qualified medical professional for health decisions.
