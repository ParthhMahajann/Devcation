from fastapi import APIRouter, Depends
from app.models.schemas import DiagnoseRequest, DiagnoseResponse, DiseaseResult
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service

router = APIRouter()


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(request: DiagnoseRequest, tg: TigerGraphService = Depends(get_tg_service)):
    raw = tg.diagnose(request.symptoms)
    diseases = []
    if raw and len(raw) > 0:
        raw_diseases = raw[0].get("diseases", [])
        for d in raw_diseases:
            diseases.append(DiseaseResult(
                disease_id=d.get("disease_id", d.get("v_id", "")),
                name=d.get("name", ""),
                icd_code=d.get("icd_code"),
                severity=d.get("severity"),
                category=d.get("category"),
                description=d.get("description"),
                score=d.get("@score", 0.0),
                match_count=d.get("@match_count", 0),
                matched_symptoms=d.get("@matched_symptoms", {}),
            ))
    return DiagnoseResponse(diseases=diseases, total=len(diseases))


@router.get("/list")
def list_symptoms(tg: TigerGraphService = Depends(get_tg_service)):
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
