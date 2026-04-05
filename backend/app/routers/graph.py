import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.models.schemas import GraphStats, GraphData, GraphNode, GraphEdge
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service
from app.limiter import limiter
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/stats", response_model=GraphStats)
@limiter.limit("60/minute")
def get_stats(request: Request, tg: TigerGraphService = Depends(get_tg_service)):
    try:
        raw = tg.get_stats()
        return GraphStats(
            disease_count=raw.get("@@disease_count", 0),
            symptom_count=raw.get("@@symptom_count", 0),
            drug_count=raw.get("@@drug_count", 0),
            side_effect_count=raw.get("@@side_effect_count", 0),
            gene_count=raw.get("@@gene_count", 0),
            patient_count=raw.get("@@patient_count", 0),
            body_system_count=raw.get("@@body_system_count", 0),
            medical_test_count=raw.get("@@medical_test_count", 0),
            biomarker_count=raw.get("@@biomarker_count", 0),
            risk_factor_count=raw.get("@@risk_factor_count", 0),
            pathway_count=raw.get("@@pathway_count", 0),
            drug_class_count=raw.get("@@drug_class_count", 0),
            procedure_count=raw.get("@@procedure_count", 0),
            has_symptom_count=raw.get("@@has_symptom_count", 0),
            treats_count=raw.get("@@treats_count", 0),
            interacts_count=raw.get("@@interacts_count", 0),
            associated_count=raw.get("@@associated_count", 0),
            comorbid_count=raw.get("@@comorbid_count", 0),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_stats failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to fetch graph statistics")


@router.get("/comorbidity/{disease_id}")
@limiter.limit("20/minute")
def comorbidity_cluster(
    request: Request,
    disease_id: str,
    max_hops: int = Query(2, ge=1, le=3),
    min_rate: float = Query(0.1, ge=0.0, le=1.0),
    tg: TigerGraphService = Depends(get_tg_service),
):
    """
    Discovers the comorbidity cluster around a disease.
    BFS on COMORBID_WITH edges, returning related diseases, shared risk factors,
    affected body systems, and drugs treating multiple cluster members.
    """
    try:
        raw = tg.comorbidity_cluster(disease_id, max_hops, min_rate)
        if not raw:
            return {"disease_id": disease_id, "cluster": []}

        result = raw[0] if isinstance(raw, list) else raw
        return {
            "disease_id":        disease_id,
            "seed_disease":      result.get("start", []),
            "cluster":           result.get("cluster", []),
            "shared_risk_factors": result.get("cluster_risk_factors", []),
            "body_systems":      result.get("cluster_systems", []),
            "common_drugs":      result.get("cluster_drugs", []),
            "top_comorbidities": result.get("@@top_comorbidities", {}),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("comorbidity_cluster failed for %s: %s", disease_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch comorbidity cluster")


@router.get("/explore")
@limiter.limit("20/minute")
def explore_graph(
    request: Request,
    center_type: Optional[str] = Query(None),
    center_id: Optional[str] = Query(None),
    max_hops: int = Query(2, ge=1, le=5),
    limit_per_hop: int = Query(20, ge=5, le=100),
    tg: TigerGraphService = Depends(get_tg_service),
):
    try:
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
            "all_diseases":   ("Disease",    "disease_id"),
            "all_symptoms":   ("Symptom",    "symptom_id"),
            "all_drugs":      ("Drug",       "drug_id"),
            "all_effects":    ("SideEffect", "effect_id"),
            "all_genes":      ("Gene",       "gene_id"),
            "all_patients":   ("Patient",    "patient_id"),
            "all_systems":    ("BodySystem", "system_id"),
            "all_tests":      ("MedicalTest","test_id"),
            "all_biomarkers": ("Biomarker",  "biomarker_id"),
            "all_risks":      ("RiskFactor", "risk_id"),
            "all_pathways":   ("Pathway",    "pathway_id"),
            "all_classes":    ("DrugClass",  "class_id"),
            "all_procs":      ("Procedure",  "procedure_id"),
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error("explore_graph failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to explore graph")
