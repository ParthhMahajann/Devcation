from fastapi import APIRouter, Depends
from app.models.schemas import DrugInteractionRequest, DrugInteractionResponse, DrugInfo, InteractionEdge
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service

router = APIRouter()


@router.post("/interactions", response_model=DrugInteractionResponse)
def check_interactions(
    request: DrugInteractionRequest,
    tg: TigerGraphService = Depends(get_tg_service),
):
    raw = tg.check_interactions(request.drug_names)
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
        return {"drug_id": drug_id, "message": "TigerGraph offline"}
    try:
        vertex = tg.conn.getVerticesById("Drug", drug_id)
        path = tg.find_treatment_path(drug_id)
        return {"drug": vertex, "treatment_path": path}
    except Exception:
        return {"drug_id": drug_id}
