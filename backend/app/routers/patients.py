import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.schemas import PatientCreate
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service
from app.limiter import limiter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{patient_id}")
@limiter.limit("30/minute")
def get_patient(request: Request, patient_id: str, tg: TigerGraphService = Depends(get_tg_service)):
    raw = tg.get_patient(patient_id)
    if not raw:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id!r} not found")
    return raw


@router.get("/{patient_id}/risk")
@limiter.limit("20/minute")
def get_patient_risk(request: Request, patient_id: str, tg: TigerGraphService = Depends(get_tg_service)):
    try:
        raw = tg.get_patient_risk(patient_id)
        if not raw:
            raise HTTPException(status_code=404, detail=f"Risk profile for {patient_id!r} not found")
        return {"patient_id": patient_id, "risk_profile": raw}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_patient_risk failed for %s: %s", patient_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch patient risk profile")


@router.post("")
@limiter.limit("10/minute")
def create_patient(request: Request, patient: PatientCreate, tg: TigerGraphService = Depends(get_tg_service)):
    try:
        result = tg.upsert_patient(patient.model_dump())
        return {"success": True, "patient": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("create_patient failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to create patient")
