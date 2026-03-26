# MedGraph AI — Day-by-Day Timeline

## Today is March 26, 2026

---

## Phase 1: Foundation (Mar 26–29)

### Day 1 — Mar 26 (TODAY) ✅ PARTIALLY DONE
- [x] Finalize idea (MedGraph AI — Healthcare Knowledge Graph)
- [x] Initialize Git repo
- [x] Create .gitignore, LICENSE
- [x] Install TigerGraph MCP + pyTigerGraph SDK
- [x] Configure .env with TigerGraph credentials
- [ ] **Create full project folder structure**
- [ ] **Set up React app (Vite + Tailwind CSS)**
- [ ] **Set up FastAPI backend skeleton**
- [ ] **Write TigerGraph GSQL schema file**
- [ ] **Write all 6 GSQL query files**

### Day 2 — Mar 27
- [ ] Create TigerGraph schema on the actual instance (via MCP or GraphStudio)
- [ ] Implement pyTigerGraph service wrapper (backend/app/services/tigergraph_service.py)
- [ ] Implement FastAPI config and dependencies
- [ ] Set up React routing, layout components (Navbar, Sidebar)
- [ ] Download open medical datasets (DrugBank, SIDER, DisGeNET)
- [ ] Start data cleaning scripts

### Day 3 — Mar 28
- [ ] Write core GSQL queries and install them on TigerGraph
- [ ] Implement API endpoints: /api/symptoms/diagnose, /api/drugs/interactions
- [ ] Build SymptomInput component (multi-select picker)
- [ ] Build DiagnosisResults component
- [ ] Clean and transform datasets into TigerGraph CSV format

### Day 4 — Mar 29
- [ ] Load full dataset into TigerGraph (5K+ diseases, 50K+ edges)
- [ ] Complete remaining API endpoints (patients, graph explorer)
- [ ] Implement GraphVisualization component (react-force-graph-2d)
- [ ] Test all queries with real data
- [ ] Generate synthetic patient data

---

## Phase 2: Integration & Polish (Mar 30 – Apr 1)

### Day 5 — Mar 30
- [ ] Full end-to-end integration (Frontend → Backend → TigerGraph)
- [ ] Test all user flows: symptom check → diagnosis → drug interactions → patient risk
- [ ] Fix bugs and edge cases

### Day 6 — Mar 31
- [ ] UI polish: loading states, error handling, responsive design
- [ ] Add graph algorithm demonstrations (PageRank results, community clusters)
- [ ] Add dashboard with statistics and quick actions
- [ ] Color theme and branding (MedGraph AI logo)

### Day 7 — Apr 1
- [ ] Final testing on all browsers
- [ ] Deploy: Vercel (frontend) + Railway (backend)
- [ ] Write comprehensive README.md with screenshots
- [ ] **Ensure team registration is complete (Round 1 deadline!)**

---

## Phase 3: Submission (Apr 2–4)

### Day 8 — Apr 2
- [ ] Create PPT (10-12 slides — see PPT_STRUCTURE.md)
- [ ] Record demo video draft (<3 min, OBS Studio)
- [ ] Clean up GitHub repo: remove secrets, add architecture diagram

### Day 9 — Apr 3
- [ ] Refine PPT based on team review
- [ ] Re-record demo video if needed
- [ ] Ensure GitHub has: clear commit history, README with screenshots, setup instructions

### Day 10 — Apr 4 ⚡ SUBMISSION DEADLINE
- [ ] Final review of ALL deliverables
- [ ] **SUBMIT: PPT + GitHub link + demo video**
- [ ] Triple-check everything works

---

## Phase 4: Mentorship (Apr 5–7)

### Days 11-13 — Apr 5–7
- [ ] Be HYPER-RESPONSIVE to mentor feedback (respond within hours)
- [ ] Implement mentor suggestions immediately
- [ ] Polish based on feedback
- [ ] This round is ELIMINATORY — treat it seriously

---

## Phase 5: Finale Prep (Apr 8–12)

### Days 14-17 — Apr 8–11
- [ ] Practice live demo (3+ dry runs)
- [ ] Prepare backup: pre-recorded demo video in case live fails
- [ ] Prepare answers for anticipated questions:
  - "Why not PostgreSQL?" → Multi-hop traversal in 12ms vs 8s with SQL JOINs
  - "How does this scale?" → TigerGraph handles billions of vertices
  - "What graph algorithms?" → PageRank, shortest path, community detection
  - "Is the data real?" → Yes, from DrugBank, SIDER, DisGeNET open datasets
- [ ] Final bug fixes

### Day 18 — Apr 12 🏆 GRAND FINALE
- [ ] **Online presentation for TigerGraph track**
- [ ] Live demo
- [ ] Answer judge questions
- [ ] WIN! 🎉
