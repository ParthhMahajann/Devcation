# MedGraph AI — Technical Architecture

## System Architecture

```
[React Frontend]  <--HTTP/REST-->  [FastAPI Backend]  <--pyTigerGraph-->  [TigerGraph DB]
     :5173                              :8000                              :9000 / :14240
       |                                  |                                    |
  - React Router                   - /api/symptoms/*                    - GSQL Queries
  - react-force-graph              - /api/drugs/*                       - Graph Algorithms
  - Tailwind CSS                   - /api/diagnose/*                    - Vertex/Edge Store
  - Axios                          - /api/graph/*                       - REST API
```

---

## 1. TigerGraph Schema Design

### Vertices
```gsql
CREATE VERTEX Disease (PRIMARY_ID disease_id STRING, name STRING, icd_code STRING,
                       severity STRING, description STRING, category STRING)

CREATE VERTEX Symptom (PRIMARY_ID symptom_id STRING, name STRING, body_system STRING,
                       severity_weight FLOAT)

CREATE VERTEX Drug (PRIMARY_ID drug_id STRING, name STRING, drug_class STRING,
                    approval_status STRING, generic_name STRING)

CREATE VERTEX SideEffect (PRIMARY_ID effect_id STRING, name STRING, severity STRING)

CREATE VERTEX Gene (PRIMARY_ID gene_id STRING, name STRING, chromosome STRING,
                    function_desc STRING)

CREATE VERTEX Patient (PRIMARY_ID patient_id STRING, age INT, gender STRING,
                       blood_type STRING, name STRING)
```

### Edges
```gsql
CREATE UNDIRECTED EDGE HAS_SYMPTOM (FROM Disease, TO Symptom, frequency STRING, weight FLOAT)
CREATE DIRECTED EDGE TREATS (FROM Drug, TO Disease, efficacy_score FLOAT, evidence_level STRING)
CREATE DIRECTED EDGE CAUSES_SIDE_EFFECT (FROM Drug, TO SideEffect, probability FLOAT)
CREATE UNDIRECTED EDGE INTERACTS_WITH (FROM Drug, TO Drug, interaction_type STRING, severity STRING)
CREATE DIRECTED EDGE TARGETS_GENE (FROM Drug, TO Gene, mechanism STRING)
CREATE DIRECTED EDGE ASSOCIATED_WITH (FROM Gene, TO Disease, evidence_strength FLOAT)
CREATE DIRECTED EDGE DIAGNOSED_WITH (FROM Patient, TO Disease, diagnosis_date DATETIME, status STRING)
CREATE DIRECTED EDGE TAKES_DRUG (FROM Patient, TO Drug, dosage STRING, start_date DATETIME)
CREATE UNDIRECTED EDGE SYMPTOM_OVERLAP (FROM Symptom, TO Symptom, correlation_score FLOAT)
```

### Graph
```gsql
CREATE GRAPH MedGraph (Disease, Symptom, Drug, SideEffect, Gene, Patient,
                       HAS_SYMPTOM, TREATS, CAUSES_SIDE_EFFECT, INTERACTS_WITH,
                       TARGETS_GENE, ASSOCIATED_WITH, DIAGNOSED_WITH, TAKES_DRUG,
                       SYMPTOM_OVERLAP)
```

---

## 2. Key GSQL Queries

### 2.1 Symptom-Based Diagnosis (Multi-hop weighted traversal)
```gsql
CREATE QUERY diagnose_from_symptoms(SET<STRING> input_symptoms) FOR GRAPH MedGraph {
  SumAccum<FLOAT> @score;
  SumAccum<INT> @match_count;

  symptoms = {Symptom.*};
  matched = SELECT s FROM symptoms:s WHERE s.name IN input_symptoms;

  diseases = SELECT d FROM matched:s -(HAS_SYMPTOM:e)- Disease:d
             ACCUM d.@score += e.weight * s.severity_weight,
                   d.@match_count += 1
             ORDER BY d.@score DESC
             LIMIT 10;

  PRINT diseases [diseases.name, diseases.@score, diseases.@match_count, diseases.severity];
}
```

### 2.2 Drug Interaction Checker (N-hop traversal)
```gsql
CREATE QUERY check_drug_interactions(SET<STRING> drug_names) FOR GRAPH MedGraph {
  SetAccum<EDGE> @@interaction_edges;

  drugs = {Drug.*};
  input_drugs = SELECT d FROM drugs:d WHERE d.name IN drug_names;

  interactions = SELECT t FROM input_drugs:s -(INTERACTS_WITH:e)- Drug:t
                 WHERE t.name IN drug_names AND t != s
                 ACCUM @@interaction_edges += e;

  PRINT interactions [interactions.name, interactions.drug_class];
  PRINT @@interaction_edges;
}
```

### 2.3 Treatment Pathway (Shortest Path)
```gsql
CREATE QUERY find_treatment_path(VERTEX<Disease> source_disease, VERTEX<Drug> target_drug) FOR GRAPH MedGraph {
  OrAccum @visited;
  SetAccum<STRING> @path;

  start = {source_disease};
  start = SELECT s FROM start:s ACCUM s.@visited = true, s.@path += s.name;

  WHILE start.size() > 0 LIMIT 5 DO
    start = SELECT t FROM start:s -(:e)- :t
            WHERE t.@visited == false
            ACCUM t.@visited = true, t.@path += s.@path, t.@path += t.name;
  END;

  result = {target_drug};
  PRINT result [result.name, result.@path];
}
```

### 2.4 Patient Risk Assessment
```gsql
CREATE QUERY patient_risk_profile(VERTEX<Patient> p) FOR GRAPH MedGraph {
  SumAccum<FLOAT> @risk_score;
  SetAccum<STRING> @risk_factors;

  patient = {p};

  diseases = SELECT d FROM patient:s -(DIAGNOSED_WITH:e)-> Disease:d;
  drugs = SELECT dr FROM patient:s -(TAKES_DRUG:e)-> Drug:dr;

  interactions = SELECT t FROM drugs:s -(INTERACTS_WITH:e)- Drug:t
                 WHERE t IN drugs AND t != s
                 ACCUM t.@risk_score += CASE WHEN e.severity == "dangerous" THEN 10
                                            WHEN e.severity == "moderate" THEN 5
                                            ELSE 1 END,
                       t.@risk_factors += s.name + " interacts with " + t.name;

  genes = SELECT g FROM diseases:d <-(ASSOCIATED_WITH:e)- Gene:g
          WHERE e.evidence_strength > 0.7;

  PRINT diseases, drugs, interactions, genes;
}
```

### 2.5 Disease PageRank
Use TigerGraph's built-in PageRank algorithm on Disease vertices connected via shared symptoms.

### 2.6 Symptom Community Detection
Use TigerGraph's built-in community detection on Symptom vertices connected via SYMPTOM_OVERLAP edges.

---

## 3. Backend Architecture (FastAPI)

### Directory Structure
```
backend/
├── requirements.txt          # fastapi, uvicorn, pyTigerGraph, pydantic, python-dotenv
├── .env.example              # TG_HOST, TG_USER, TG_PASSWORD, TG_GRAPH
└── app/
    ├── __init__.py
    ├── main.py               # FastAPI app entry point with CORS
    ├── config.py             # Settings from env vars using pydantic-settings
    ├── dependencies.py       # Dependency injection for TG service
    ├── models/
    │   ├── __init__.py
    │   └── schemas.py        # Pydantic request/response models
    ├── services/
    │   ├── __init__.py
    │   ├── tigergraph_service.py  # pyTigerGraph wrapper (connection, query runners)
    │   ├── diagnosis_service.py   # Business logic for diagnosis
    │   └── drug_service.py        # Drug interaction logic
    └── routers/
        ├── __init__.py
        ├── symptoms.py       # POST /api/symptoms/diagnose, GET /api/symptoms/list
        ├── drugs.py          # POST /api/drugs/interactions, GET /api/drugs/list, GET /api/drugs/{id}
        ├── patients.py       # GET /api/patients/{id}/risk, POST /api/patients
        └── graph.py          # GET /api/graph/stats, GET /api/graph/explore
```

### Key Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/symptoms/diagnose` | Input symptoms → ranked diagnoses |
| GET | `/api/symptoms/list` | List all symptoms (for autocomplete) |
| POST | `/api/drugs/interactions` | Input drug list → interaction network |
| GET | `/api/drugs/list` | List all drugs (for search) |
| GET | `/api/drugs/{id}` | Drug details with side effects |
| GET | `/api/patients/{id}/risk` | Patient risk profile |
| POST | `/api/patients` | Create/update patient |
| GET | `/api/graph/stats` | Graph statistics (vertex/edge counts) |
| GET | `/api/graph/explore` | Get subgraph for visualization |

### pyTigerGraph Service
```python
import pyTigerGraph as tg

class TigerGraphService:
    def __init__(self):
        self.conn = tg.TigerGraphConnection(
            host="http://122.179.90.210",
            graphname="MedGraph",
            restppPort="9000",
            gsPort="14240",
            apiToken="<from .env>"
        )

    def diagnose(self, symptoms: list[str]) -> dict:
        return self.conn.runInstalledQuery("diagnose_from_symptoms",
                                           {"input_symptoms": symptoms})

    def check_interactions(self, drugs: list[str]) -> dict:
        return self.conn.runInstalledQuery("check_drug_interactions",
                                           {"drug_names": drugs})

    def get_patient_risk(self, patient_id: str) -> dict:
        return self.conn.runInstalledQuery("patient_risk_profile",
                                           {"p": patient_id})
```

---

## 4. Frontend Architecture (React + Vite)

### Directory Structure
```
frontend/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── .env.example              # VITE_API_URL=http://localhost:8000
├── index.html
├── public/
│   ├── favicon.ico
│   └── logo.png
└── src/
    ├── main.jsx
    ├── App.jsx               # Router setup
    ├── api/
    │   ├── client.js         # Axios instance with base URL
    │   ├── symptoms.js       # Symptom API calls
    │   ├── drugs.js          # Drug API calls
    │   ├── patients.js       # Patient API calls
    │   └── graph.js          # Graph API calls
    ├── components/
    │   ├── layout/
    │   │   ├── Navbar.jsx
    │   │   ├── Sidebar.jsx
    │   │   └── Footer.jsx
    │   ├── graph/
    │   │   ├── GraphVisualization.jsx  # Force-directed graph (react-force-graph-2d)
    │   │   ├── NodeTooltip.jsx
    │   │   └── GraphControls.jsx
    │   ├── diagnosis/
    │   │   ├── SymptomInput.jsx   # Multi-select symptom picker
    │   │   ├── DiagnosisResults.jsx
    │   │   └── ConfidenceBar.jsx
    │   ├── drugs/
    │   │   ├── DrugSearch.jsx
    │   │   ├── InteractionNetwork.jsx
    │   │   └── InteractionAlert.jsx
    │   ├── patient/
    │   │   ├── PatientCard.jsx
    │   │   └── RiskDashboard.jsx
    │   └── common/
    │       ├── LoadingSpinner.jsx
    │       ├── ErrorBoundary.jsx
    │       └── StatsCard.jsx
    ├── pages/
    │   ├── Dashboard.jsx
    │   ├── DiagnosePage.jsx
    │   ├── InteractionsPage.jsx
    │   ├── PatientPage.jsx
    │   ├── ExplorePage.jsx
    │   └── AboutPage.jsx
    ├── hooks/
    │   ├── useGraphData.js
    │   └── useDiagnosis.js
    ├── utils/
    │   ├── graphHelpers.js   # Node coloring, sizing logic
    │   └── formatters.js
    └── styles/
        └── globals.css       # Tailwind imports + custom styles
```

### Key Pages
1. **Dashboard** (`/`) — Overview stats, graph summary, quick actions
2. **Symptom Checker** (`/diagnose`) — Input symptoms, see ranked diagnoses with confidence scores
3. **Drug Interactions** (`/interactions`) — Input medications, see interaction network graph
4. **Patient Profile** (`/patient/:id`) — Risk assessment, medication list, disease history
5. **Graph Explorer** (`/explore`) — Interactive force-directed graph of entire knowledge graph
6. **About** (`/about`) — Project description, team, tech stack

### Key Libraries
- `react-force-graph-2d` — Interactive graph visualization
- `axios` — HTTP client
- `tailwindcss` — Utility-first CSS
- `react-router-dom` — Client-side routing
- `recharts` — Charts for dashboard
- `react-select` — Multi-select dropdowns for symptom/drug input

---

## 5. Data Pipeline

### Open Data Sources
| Dataset | Content | URL |
|---------|---------|-----|
| DrugBank (open) | Drug-drug interactions, drug info | https://go.drugbank.com/releases/latest |
| SIDER | Drug side effects | http://sideeffects.embl.de/ |
| DisGeNET | Gene-disease associations | https://www.disgenet.org/ |
| Disease Ontology | Disease hierarchy, ICD codes | https://disease-ontology.org/ |
| Synthetic | Patient data for demo | Generated with Python script |

### Data Pipeline Scripts
```
data/
├── raw/                      # Downloaded datasets (gitignored)
├── processed/
│   ├── vertices/
│   │   ├── diseases.csv      # disease_id, name, icd_code, severity, description, category
│   │   ├── symptoms.csv      # symptom_id, name, body_system, severity_weight
│   │   ├── drugs.csv         # drug_id, name, drug_class, approval_status, generic_name
│   │   ├── side_effects.csv  # effect_id, name, severity
│   │   ├── genes.csv         # gene_id, name, chromosome, function_desc
│   │   └── patients.csv      # patient_id, age, gender, blood_type, name
│   └── edges/
│       ├── has_symptom.csv
│       ├── treats.csv
│       ├── causes_side_effect.csv
│       ├── interacts_with.csv
│       ├── targets_gene.csv
│       ├── associated_with.csv
│       ├── diagnosed_with.csv
│       ├── takes_drug.csv
│       └── symptom_overlap.csv
└── scripts/
    ├── download_data.py      # Download open datasets
    ├── clean_data.py         # Transform raw → processed CSVs
    └── generate_synthetic.py # Generate synthetic patient data
```

### Target Data Volume
- 5,000+ diseases
- 10,000+ symptoms
- 3,000+ drugs
- 500+ genes
- 50,000+ edges
- 100 synthetic patients

---

## 6. Deployment

| Component | Platform | Notes |
|-----------|----------|-------|
| TigerGraph | Savanna Cloud / User's server | Already running at 122.179.90.210 |
| FastAPI Backend | Railway.app or Render | Free tier, auto-deploy from GitHub |
| React Frontend | Vercel | Free, instant deploy |
| Backup | Run locally | If deployed version has issues during demo |
