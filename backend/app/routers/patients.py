from fastapi import APIRouter, Depends
from app.models.schemas import PatientCreate
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service

router = APIRouter()


@router.get("/{patient_id}")
def get_patient(patient_id: str, tg: TigerGraphService = Depends(get_tg_service)):
    raw = tg.get_patient(patient_id)
    return raw


@router.get("/{patient_id}/risk")
def get_patient_risk(patient_id: str, tg: TigerGraphService = Depends(get_tg_service)):
    raw = tg.get_patient_risk(patient_id)
    return {"patient_id": patient_id, "risk_profile": raw}


@router.post("")
def create_patient(patient: PatientCreate, tg: TigerGraphService = Depends(get_tg_service)):
    result = tg.upsert_patient(patient.model_dump())
    return {"success": True, "patient": result}
