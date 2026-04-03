import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.schemas import DrugInteractionRequest, DrugInteractionResponse, DrugInfo, InteractionEdge
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service
from app.limiter import limiter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/interactions", response_model=DrugInteractionResponse)
@limiter.limit("30/minute")
def check_interactions(
    request: Request,
    body: DrugInteractionRequest,
    tg: TigerGraphService = Depends(get_tg_service),
):
    raw = tg.check_interactions(body.drug_names)
    drugs = []
    interactions = []

    if raw and len(raw) > 0:
        raw_drugs = raw[0].get("all_drugs", [])
        for d in raw_drugs:
            attrs = d.get("attributes", d)
            drugs.append(DrugInfo(
                drug_id=attrs.get("drug_id", d.get("v_id", "")),
                name=attrs.get("name", ""),
                drug_class=attrs.get("drug_class"),
                approval_status=attrs.get("approval_status"),
                generic_name=attrs.get("generic_name"),
            ))

        raw_edges = raw[0].get("@@interaction_edges", [])
        for e in raw_edges:
            interactions.append(InteractionEdge(
                from_drug=e.get("from_id", ""),
                to_drug=e.get("to_id", ""),
                interaction_type=e.get("attributes", {}).get("interaction_type"),
                severity=e.get("attributes", {}).get("severity"),
            ))

    return DrugInteractionResponse(drugs=drugs, interactions=interactions)


@router.get("/list")
def list_drugs(tg: TigerGraphService = Depends(get_tg_service)):
    drugs = tg.list_drugs()
    result = []
    for d in drugs:
        attrs = d.get("attributes", {})
        result.append({
            "drug_id": d.get("v_id", ""),
            "name": attrs.get("name", ""),
            "drug_class": attrs.get("drug_class", ""),
            "approval_status": attrs.get("approval_status", ""),
            "generic_name": attrs.get("generic_name", ""),
        })
    return {"drugs": result, "total": len(result)}


@router.get("/{drug_id}")
def get_drug(drug_id: str, tg: TigerGraphService = Depends(get_tg_service)):
    if not tg.conn:
        raise HTTPException(status_code=503, detail="Database unavailable")
    try:
        vertex = tg.conn.getVerticesById("Drug", drug_id)
        if not vertex:
            raise HTTPException(status_code=404, detail=f"Drug {drug_id!r} not found")
        path = tg.find_treatment_path(drug_id)
        return {"drug": vertex, "treatment_path": path}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_drug failed for %s: %s", drug_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch drug data")
