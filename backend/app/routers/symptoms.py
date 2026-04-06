import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.schemas import DiagnoseRequest, DiagnoseResponse, DiseaseResult
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service
from app.limiter import limiter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/diagnose", response_model=DiagnoseResponse)
@limiter.limit("30/minute")
def diagnose(request: Request, body: DiagnoseRequest, tg: TigerGraphService = Depends(get_tg_service)):
    try:
        raw = tg.diagnose(body.symptoms)
        diseases = []
        if raw and len(raw) > 0:
            # GSQL query prints variable named "results", so key is "results"
            raw_diseases = raw[0].get("results", raw[0].get("diseases", []))
            for d in raw_diseases:
                attrs = d.get("attributes", d)
                diseases.append(DiseaseResult(
                    disease_id=attrs.get("disease_id", d.get("v_id", "")),
                    name=attrs.get("name", ""),
                    icd_code=attrs.get("icd10_code", attrs.get("icd_code")),
                    severity=attrs.get("severity"),
                    category=attrs.get("category"),
                    description=attrs.get("description"),
                    score=attrs.get("@direct_score", 0.0) + attrs.get("@indirect_score", 0.0),
                    match_count=attrs.get("@match_count", 0),
                    matched_symptoms=attrs.get("@matched_symptoms", {}),
                ))
        return DiagnoseResponse(diseases=diseases, total=len(diseases))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("diagnose failed: %s", e)
        raise HTTPException(status_code=500, detail="Diagnosis failed")


@router.get("/list")
@limiter.limit("60/minute")
def list_symptoms(request: Request, tg: TigerGraphService = Depends(get_tg_service)):
    try:
        symptoms = tg.list_symptoms()
        result = []
        for s in symptoms:
            attrs = s.get("attributes", {})
            result.append({
                "symptom_id": s.get("v_id", ""),
                "name": attrs.get("name", ""),
                "body_system": attrs.get("body_system", ""),
                "severity_weight": attrs.get("severity_weight", 0.5),
            })
        return {"symptoms": result, "total": len(result)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("list_symptoms failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to fetch symptoms")
