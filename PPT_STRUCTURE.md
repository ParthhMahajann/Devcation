# MedGraph AI — PPT Structure (10-12 slides)

## Slide 1: Title
- **MedGraph AI** — Intelligent Healthcare Knowledge Graph
- Team name, track (TigerGraph), team members
- Devcation Delhi 2026

## Slide 2: The Problem
- Drug interactions kill 100K+ people/year in the US alone
- Existing systems check only direct (1-hop) interactions
- Multi-hop interactions through shared genes, metabolic pathways are missed
- Doctors manage patients on 5+ medications — complexity explodes
- Use a real, impactful statistic

## Slide 3: Our Solution
- One-sentence pitch: "MedGraph AI uses TigerGraph's multi-hop traversal to detect hidden drug interactions and provide intelligent clinical decision support"
- Key screenshot of the app
- Highlight: real-time, graph-powered, visual

## Slide 4: Why Graph? (THIS SLIDE WINS POINTS)
- Side-by-side comparison:
  - SQL: "Finding a 3-hop drug interaction requires 3 JOINs, takes 8+ seconds on 100K rows"
  - TigerGraph: "Same query = 2-hop traversal, completes in 12ms"
- Healthcare data is inherently a graph: diseases → symptoms → drugs → genes
- Relational databases cannot efficiently model these relationships

## Slide 5: Architecture
- Clean diagram: React ↔ FastAPI ↔ TigerGraph
- Show the full tech stack visually
- Highlight: TigerGraph Savanna Cloud, pyTigerGraph SDK, GSQL

## Slide 6: Graph Schema
- Visual diagram of vertices and edges (from GraphStudio or custom)
- 6 vertex types, 9 edge types
- Show the richness of the medical knowledge graph

## Slide 7: Key Features (with screenshots)
1. Symptom Checker — multi-hop weighted traversal
2. Drug Interaction Network — N-hop detection + visualization
3. Treatment Pathway Explorer — shortest path algorithm
4. Patient Risk Assessment — combined risk scoring

## Slide 8: Graph Algorithms Used
- **PageRank** — Rank diseases by importance/connectivity
- **Shortest Path** — Find treatment pathways between diseases and drugs
- **Community Detection** — Discover symptom clusters
- **Jaccard Similarity** — Find overlapping symptom patterns
- Name them explicitly — judges are TigerGraph people!

## Slide 9: Live Demo / Screenshots
- Key user flow walkthrough
- Show the interactive graph visualization prominently
- Show real data (not toy data)

## Slide 10: Data & Scale
- Open medical datasets: DrugBank, SIDER, DisGeNET
- Data volume: 5K+ diseases, 10K+ symptoms, 3K+ drugs, 50K+ edges
- Real, validated medical data — not synthetic

## Slide 11: Impact & Future Scope
- Real-world deployment potential in hospitals/pharmacies
- Integration with Electronic Health Records (EHR)
- Expansion: add more data sources, clinical trials, patient outcomes
- Scalability: TigerGraph handles billions of vertices

## Slide 12: Thank You
- GitHub repo link
- Demo video link
- Team contact info
- "Built with TigerGraph 💙"
