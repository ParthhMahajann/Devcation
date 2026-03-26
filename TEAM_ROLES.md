# MedGraph AI — Team Roles & Division

## Team of 3-4 Members

### Member 1: Graph Engineer + Backend Lead
**Primary:** TigerGraph schema, GSQL queries, pyTigerGraph integration
- Design and create TigerGraph schema (vertices, edges, graph)
- Write and install all GSQL queries (diagnose, interactions, pathways, risk)
- Implement graph algorithms (PageRank, shortest path, community detection)
- Write data loading scripts/jobs
- Help with backend pyTigerGraph service wrapper

### Member 2: Backend API Developer
**Primary:** FastAPI endpoints, business logic, API documentation
- Set up FastAPI project structure with CORS, error handling
- Implement all API routers (symptoms, drugs, patients, graph)
- Create Pydantic request/response models
- Write data processing and transformation logic
- API documentation via Swagger/OpenAPI
- **If only 3 members:** Also handles data prep and PPT/presentation

### Member 3: Frontend Developer
**Primary:** React UI, graph visualization, dashboard, UX
- Set up React app with Vite + Tailwind CSS
- Build all 6 pages (Dashboard, Diagnose, Interactions, Patient, Explore, About)
- Implement graph visualization using react-force-graph-2d
- Create reusable components (SymptomInput, DiagnosisResults, InteractionNetwork)
- Responsive design, loading states, error boundaries
- Polish the UI for demo day

### Member 4: Data + Presentation Lead
**Primary:** Data sourcing/cleaning, PPT, demo video, documentation
- Source and download open medical datasets (DrugBank, SIDER, DisGeNET)
- Write Python scripts to clean and transform data into TigerGraph CSVs
- Generate synthetic patient data for demo
- Create the PPT (10-12 slides, see PPT_STRUCTURE.md)
- Record demo video (<3 minutes, OBS Studio)
- Write comprehensive README.md with screenshots and setup instructions
- Maintain GitHub repo quality (commit messages, branches, docs)

---

## Communication Plan
- Daily standup (15 min) — what you did, what you'll do, blockers
- Use a shared group chat (WhatsApp/Discord) for quick questions
- Push code frequently — no big bang merges
- Code review before merging to main branch
