# MedGraph AI — Devcation Delhi 2026 (TigerGraph Track)

## Project Overview
**MedGraph AI** is an intelligent Healthcare Knowledge Graph & Clinical Decision Support system built for the **Devcation Delhi 2026 hackathon** (TigerGraph Premium Track).

It connects diseases, symptoms, drugs, side-effects, genes, and patient profiles into a graph database. Users can input symptoms to get graph-powered differential diagnoses, drug interaction alerts, and personalized treatment pathways using TigerGraph's multi-hop traversal.

---

## Hackathon Details
- **Event:** Devcation Delhi 2026 (GDG IGDTUW + GDG IIT Delhi)
- **Track:** TigerGraph (Premium Track)
- **Prizes:** 1st Place ₹24,000, 2nd Place ₹12,000
- **Team Size:** 3-4 members
- **Problem Statement:** OPEN — build anything using TigerGraph as primary database
- **Bonus Points:** Graph-native features (recommendation, fraud detection, social network analysis, supply chain, healthcare knowledge graph, skill pathfinder, financial risk)

### Key Dates
| Round | Timeline | Mode |
|-------|----------|------|
| Round 1: Registration | March 15 – April 1 | Online |
| Round 2: Submission (PPT + GitHub + demo video) | April 2 – April 4 | Online |
| Round 3: Mentorship (eliminatory) | April 5 – April 7 | Online (Google Meet) |
| Round 4: Grand Finale | April 12, 11AM–6PM | Online for TigerGraph track |

### Submission Requirements
- PPT presentation
- GitHub repository link
- Demo video (optional but recommended)

---

## Why MedGraph AI Wins
1. **Maximum graph-native bonus** — Hits Healthcare Knowledge Graph + Recommendation System + 3 graph algorithms (PageRank, shortest path, community detection)
2. **Real-world impact** — Drug interactions kill 100K+ people/year
3. **Visually stunning** — Interactive force-directed graph of medical networks
4. **Open data available** — DrugBank, SIDER, DisGeNET
5. **Clear "Why Graph?" story** — Multi-hop drug interaction detection is impossible in SQL at speed

---

## Tech Stack
| Component | Technology |
|-----------|-----------|
| Database | TigerGraph Savanna Cloud (primary) + Docker Community Edition (backup) |
| Backend | Python FastAPI + pyTigerGraph SDK |
| Frontend | React (Vite) + react-force-graph-2d + Tailwind CSS + Axios |
| Deployment | Vercel (frontend) + Railway/Render (backend) |

---

## Core Features
1. **Symptom Checker** — Input symptoms → ranked differential diagnoses via weighted multi-hop traversal
2. **Drug Interaction Network** — Visualize dangerous drug combinations up to N hops
3. **Treatment Pathway Explorer** — Graph viz: Disease → Drug → SideEffect → overlapping conditions
4. **Patient Risk Assessment** — Genetic risk factors via Gene-Disease associations
5. **Interactive Graph Explorer** — Force-directed graph of the entire medical knowledge graph

---

## TigerGraph Configuration
- **Host:** http://122.179.90.210
- **Graph Name:** MedGraph
- **REST++ Port:** 9000
- **GraphStudio Port:** 14240
- **Credentials:** Stored in `.env` file (gitignored)
- **MCP:** TigerGraph MCP server configured in Claude Code as `tigergraph`
- **SDK:** pyTigerGraph-mcp[llm] installed

---

## What's Done So Far
- [x] Git repo initialized
- [x] `.gitignore` created
- [x] `LICENSE` (MIT) created
- [x] `.env` file with TigerGraph credentials (gitignored)
- [x] TigerGraph MCP installed and configured in Claude Code
- [x] pyTigerGraph SDK installed
- [ ] Project folder structure (backend + frontend + tigergraph)
- [ ] React app scaffolding (Vite + Tailwind)
- [ ] FastAPI backend scaffolding
- [ ] TigerGraph schema (GSQL)
- [ ] GSQL queries
- [ ] Data pipeline scripts
- [ ] API endpoints
- [ ] Frontend pages & components
- [ ] Graph visualization
- [ ] Integration & testing
- [ ] PPT & demo video
