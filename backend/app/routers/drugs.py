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
    try:
        raw = tg.check_interactions(body.drug_names)
        drugs = []
        interactions = []

        if raw and len(raw) > 0:
            # GSQL query has multiple PRINT statements, producing a list of dicts.
            # Merge all result dicts so we can look up any key.
            merged = {}
            for entry in raw:
                if isinstance(entry, dict):
                    merged.update(entry)

            # Drug list: GSQL prints as "all_input" (not "all_drugs")
            raw_drugs = merged.get("all_input", merged.get("all_drugs", []))
            for d in raw_drugs:
                attrs = d.get("attributes", d)
                drugs.append(DrugInfo(
                    drug_id=attrs.get("drug_id", d.get("v_id", "")),
                    name=attrs.get("name", ""),
                    drug_class=attrs.get("drug_class"),
                    approval_status=attrs.get("approval_status"),
                    generic_name=attrs.get("generic_name"),
                ))

            raw_edges = merged.get("@@interaction_edges", [])
            for e in raw_edges:
                interactions.append(InteractionEdge(
                    from_drug=e.get("from_id", ""),
                    to_drug=e.get("to_id", ""),
                    interaction_type=e.get("attributes", {}).get("interaction_type"),
                    severity=e.get("attributes", {}).get("severity"),
                ))

        return DrugInteractionResponse(drugs=drugs, interactions=interactions)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("check_interactions failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to check drug interactions")


@router.get("/list")
@limiter.limit("60/minute")
def list_drugs(request: Request, tg: TigerGraphService = Depends(get_tg_service)):
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error("list_drugs failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to fetch drugs")


@router.get("/{drug_id}")
@limiter.limit("60/minute")
def get_drug(request: Request, drug_id: str, tg: TigerGraphService = Depends(get_tg_service)):
    if not tg.conn:
        raise HTTPException(status_code=503, detail="Database unavailable")
    try:
        vertex = tg.conn.getVerticesById("Drug", drug_id)
        if not vertex:
            raise HTTPException(status_code=404, detail=f"Drug {drug_id!r} not found")
        attrs = vertex[0].get("attributes", {})
        drug_data = {
            "drug_id": vertex[0].get("v_id", drug_id),
            **attrs,
        }
        return {"drug": drug_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_drug failed for %s: %s", drug_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch drug data")
