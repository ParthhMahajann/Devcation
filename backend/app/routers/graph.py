from fastapi import APIRouter, Depends, Query
from app.models.schemas import GraphStats, GraphData, GraphNode, GraphEdge
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service
from typing import Optional

router = APIRouter()


@router.get("/stats", response_model=GraphStats)
def get_stats(tg: TigerGraphService = Depends(get_tg_service)):
    raw = tg.get_stats()
    return GraphStats(
        disease_count=raw.get("@@disease_count", 0),
        symptom_count=raw.get("@@symptom_count", 0),
        drug_count=raw.get("@@drug_count", 0),
        side_effect_count=raw.get("@@side_effect_count", 0),
        gene_count=raw.get("@@gene_count", 0),
        patient_count=raw.get("@@patient_count", 0),
    )


@router.get("/explore")
def explore_graph(
    center_type: Optional[str] = Query(None),
    center_id: Optional[str] = Query(None),
    max_hops: int = Query(2, ge=1, le=5),
    limit_per_hop: int = Query(20, ge=5, le=100),
    tg: TigerGraphService = Depends(get_tg_service),
):
    raw = tg.explore_subgraph(
        center_type=center_type or "",
        center_id=center_id or "",
        max_hops=max_hops,
        limit_per_hop=limit_per_hop,
    )

    nodes = []
    edges = []

    # Parse each vertex type from the result
    type_map = {
        "all_diseases": ("Disease", "disease_id"),
        "all_symptoms": ("Symptom", "symptom_id"),
        "all_drugs":    ("Drug",    "drug_id"),
        "all_effects":  ("SideEffect", "effect_id"),
        "all_genes":    ("Gene",    "gene_id"),
    }

    if raw and len(raw) > 0:
        result = raw[0] if isinstance(raw, list) else raw
        for key, (vtype, id_field) in type_map.items():
            for v in result.get(key, []):
                nodes.append(GraphNode(
                    id=v.get(id_field, v.get("v_id", "")),
                    label=v.get("name", ""),
                    type=vtype,
                    properties={k: v[k] for k in v if k not in (id_field, "name")},
                ))

        for e in result.get("@@all_edges", []):
            edges.append(GraphEdge(
                source=e.get("from_id", ""),
                target=e.get("to_id", ""),
                type=e.get("e_type", ""),
                properties=e.get("attributes", {}),
            ))

    return GraphData(nodes=nodes, edges=edges)
