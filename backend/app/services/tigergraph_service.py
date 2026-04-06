import logging
import pyTigerGraph as tg
from fastapi import HTTPException
from app.config import get_settings

logger = logging.getLogger(__name__)


def _db_unavailable():
    """Raise 503 or return True (to signal mock mode)."""
    if get_settings().use_mock_data:
        return True   # caller should use mock data
    raise HTTPException(status_code=503, detail="Database unavailable — TigerGraph is not connected")


class TigerGraphService:
    def __init__(self):
        settings = get_settings()
        try:
            self.conn = tg.TigerGraphConnection(
                host=settings.tg_host,
                graphname=settings.tg_graph,
                restppPort=settings.tg_restpp_port,
                gsPort=settings.tg_gs_port,
                username=settings.tg_username,
                password=settings.tg_password,
            )
            # Token acquisition: API token > explicit secret > auto-create secret
            if settings.tg_api_token:
                self.conn.apiToken = settings.tg_api_token
            elif settings.tg_secret:
                self.conn.getToken(settings.tg_secret)
            else:
                try:
                    secret = self.conn.createSecret()
                    self.conn.getToken(secret)
                except Exception as token_err:
                    # Local CE may not require a token — proceed without one
                    logger.warning("Token acquisition skipped: %s", token_err)
            logger.info("TigerGraph connected → %s/%s", settings.tg_host, settings.tg_graph)
        except Exception as e:
            logger.error("TigerGraph connection failed: %s", e)
            self.conn = None

    # ─── Diagnosis ─────────────────────────────────────────────────────────────

    def diagnose(self, symptoms: list[str]) -> dict:
        if not self.conn:
            if _db_unavailable():
                return self._mock_diagnose(symptoms)
        try:
            return self.conn.runInstalledQuery(
                "diagnose_from_symptoms",
                {"input_symptoms": symptoms}
            )
        except Exception as e:
            logger.error("diagnose query failed: %s", e)
            raise HTTPException(status_code=500, detail="Diagnosis query failed")

    # ─── Drug Interactions ──────────────────────────────────────────────────────

    def check_interactions(self, drug_names: list[str]) -> dict:
        if not self.conn:
            if _db_unavailable():
                return self._mock_interactions(drug_names)
        try:
            return self.conn.runInstalledQuery(
                "check_drug_interactions",
                {"drug_names": drug_names}
            )
        except Exception as e:
            logger.error("check_drug_interactions query failed: %s", e)
            raise HTTPException(status_code=500, detail="Drug interaction query failed")

    # ─── Treatment Path ─────────────────────────────────────────────────────────

    def find_treatment_path(self, disease_id: str) -> dict:
        if not self.conn:
            if _db_unavailable():
                return {}
            return {}
        try:
            return self.conn.runInstalledQuery(
                "find_treatment_path",
                {"source_disease": disease_id}
            )
        except Exception as e:
            logger.error("find_treatment_path query failed for %s: %s", disease_id, e)
            raise HTTPException(status_code=500, detail="Treatment path query failed")

    # ─── Patient Risk ───────────────────────────────────────────────────────────

    def get_patient_risk(self, patient_id: str) -> dict:
        if not self.conn:
            if _db_unavailable():
                return self._mock_patient_risk(patient_id)
            return {}
        try:
            return self.conn.runInstalledQuery(
                "patient_risk_profile",
                {"p": patient_id}
            )
        except Exception as e:
            logger.error("patient_risk_profile query failed for %s: %s", patient_id, e)
            raise HTTPException(status_code=500, detail="Patient risk profile query failed")

    # ─── Graph Stats ────────────────────────────────────────────────────────────

    def get_stats(self) -> dict:
        if not self.conn:
            if _db_unavailable():
                return self._mock_stats()
        try:
            result = self.conn.runInstalledQuery("get_graph_stats", {})
            return result[0] if result else {}
        except Exception as e:
            logger.error("get_graph_stats query failed: %s", e)
            raise HTTPException(status_code=500, detail="Graph stats query failed")

    # ─── Graph Explorer ─────────────────────────────────────────────────────────

    def explore_subgraph(
        self,
        center_type: str = "",
        center_id: str = "",
        max_hops: int = 2,
        limit_per_hop: int = 20,
    ) -> dict:
        if not self.conn:
            if _db_unavailable():
                return []
            return []
        try:
            return self.conn.runInstalledQuery(
                "explore_subgraph",
                {
                    "center_type": center_type,
                    "center_id": center_id,
                    "max_hops": max_hops,
                    "limit_per_hop": limit_per_hop,
                }
            )
        except Exception as e:
            logger.error("explore_subgraph query failed: %s", e)
            raise HTTPException(status_code=500, detail="Graph exploration query failed")

    # ─── Pharmacogenomics ────────────────────────────────────────────────────────

    def pharmacogenomics_report(self, patient_id: str) -> dict:
        if not self.conn:
            if _db_unavailable():
                return self._mock_pgx(patient_id)
            return {}
        try:
            return self.conn.runInstalledQuery(
                "pharmacogenomics_report",
                {"p": patient_id}
            )
        except Exception as e:
            logger.error("pharmacogenomics_report query failed for %s: %s", patient_id, e)
            raise HTTPException(status_code=500, detail="Pharmacogenomics report failed")

    # ─── Disease Progression ─────────────────────────────────────────────────────

    def disease_progression_risk(self, patient_id: str, max_depth: int = 3) -> dict:
        if not self.conn:
            if _db_unavailable():
                return self._mock_progression(patient_id)
            return {}
        try:
            return self.conn.runInstalledQuery(
                "disease_progression_risk",
                {"p": patient_id, "max_depth": max_depth}
            )
        except Exception as e:
            logger.error("disease_progression_risk query failed for %s: %s", patient_id, e)
            raise HTTPException(status_code=500, detail="Disease progression query failed")

    # ─── Comorbidity Cluster ─────────────────────────────────────────────────────

    def comorbidity_cluster(self, disease_id: str, max_hops: int = 2, min_rate: float = 0.1) -> dict:
        if not self.conn:
            if _db_unavailable():
                return self._mock_comorbidity(disease_id)
            return {}
        try:
            return self.conn.runInstalledQuery(
                "comorbidity_cluster",
                {"seed_disease": disease_id, "max_hops": max_hops, "min_rate": min_rate}
            )
        except Exception as e:
            logger.error("comorbidity_cluster query failed for %s: %s", disease_id, e)
            raise HTTPException(status_code=500, detail="Comorbidity cluster query failed")

    # ─── Contraindication Safety Check ───────────────────────────────────────────

    def contraindication_safety_check(self, patient_id: str, proposed_drugs: list[str]) -> dict:
        if not self.conn:
            if _db_unavailable():
                return self._mock_safety_check(patient_id)
            return {}
        try:
            return self.conn.runInstalledQuery(
                "contraindication_safety_check",
                {"p": patient_id, "proposed_drug_names": proposed_drugs}
            )
        except Exception as e:
            logger.error("contraindication_safety_check query failed for %s: %s", patient_id, e)
            raise HTTPException(status_code=500, detail="Safety check query failed")

    # ─── List helpers ───────────────────────────────────────────────────────────

    def list_symptoms(self) -> list:
        if not self.conn:
            if _db_unavailable():
                return self._mock_symptoms()
        try:
            return self.conn.getVertices("Symptom")
        except Exception as e:
            logger.error("list_symptoms failed: %s", e)
            raise HTTPException(status_code=500, detail="Failed to list symptoms")

    def list_drugs(self) -> list:
        if not self.conn:
            if _db_unavailable():
                return self._mock_drugs()
        try:
            return self.conn.getVertices("Drug")
        except Exception as e:
            logger.error("list_drugs failed: %s", e)
            raise HTTPException(status_code=500, detail="Failed to list drugs")

    # ─── Patient CRUD ────────────────────────────────────────────────────────────

    def get_patient(self, patient_id: str) -> dict:
        if not self.conn:
            if _db_unavailable():
                return {"patient_id": patient_id, "name": "Demo Patient", "age": 45,
                        "gender": "Male", "blood_type": "O+",
                        "conditions": [{"name": "Hypertension", "severity": "moderate", "status": "active"}],
                        "medications": [{"name": "Lisinopril", "dosage": "10mg daily", "start_date": "2025-01-15"}],
                        "drug_interactions": []}
        try:
            vertices = self.conn.getVerticesById("Patient", patient_id)
            if not vertices:
                return None

            vertex = vertices[0]
            result = {
                "patient_id": vertex.get("v_id", patient_id),
                **vertex.get("attributes", {}),
            }

            # Fetch conditions (DIAGNOSED_WITH → Disease)
            conditions = []
            try:
                diag_edges = self.conn.getEdges("Patient", patient_id, "DIAGNOSED_WITH")
                for edge in diag_edges:
                    target_id = edge.get("to_id", "")
                    edge_attrs = edge.get("attributes", {})
                    disease_name = target_id
                    severity = ""
                    try:
                        disease_verts = self.conn.getVerticesById("Disease", target_id)
                        if disease_verts:
                            disease_name = disease_verts[0].get("attributes", {}).get("name", target_id)
                            severity = disease_verts[0].get("attributes", {}).get("severity", "")
                    except Exception:
                        pass
                    conditions.append({
                        "name": disease_name,
                        "severity": severity,
                        "status": edge_attrs.get("status", ""),
                    })
            except Exception as edge_err:
                logger.warning("Failed to fetch conditions for %s: %s", patient_id, edge_err)
            result["conditions"] = conditions

            # Fetch medications (TAKES_DRUG → Drug)
            medications = []
            drug_id_to_name = {}
            try:
                drug_edges = self.conn.getEdges("Patient", patient_id, "TAKES_DRUG")
                for edge in drug_edges:
                    target_id = edge.get("to_id", "")
                    edge_attrs = edge.get("attributes", {})
                    drug_name = target_id
                    try:
                        drug_verts = self.conn.getVerticesById("Drug", target_id)
                        if drug_verts:
                            drug_name = drug_verts[0].get("attributes", {}).get("name", target_id)
                    except Exception:
                        pass
                    drug_id_to_name[target_id] = drug_name
                    medications.append({
                        "name": drug_name,
                        "dosage": edge_attrs.get("dosage", ""),
                        "start_date": edge_attrs.get("start_date", ""),
                    })
            except Exception as edge_err:
                logger.warning("Failed to fetch medications for %s: %s", patient_id, edge_err)
            result["medications"] = medications

            # Check drug-drug interactions among current medications
            drug_interactions = []
            drug_ids = list(drug_id_to_name.keys())
            if len(drug_ids) >= 2:
                try:
                    checked_pairs = set()
                    for d1_id in drug_ids:
                        edges = self.conn.getEdges("Drug", d1_id, "INTERACTS_WITH")
                        for edge in edges:
                            d2_id = edge.get("to_id", "")
                            if d2_id in drug_id_to_name:
                                pair = tuple(sorted([d1_id, d2_id]))
                                if pair not in checked_pairs:
                                    checked_pairs.add(pair)
                                    edge_attrs = edge.get("attributes", {})
                                    drug_interactions.append({
                                        "from_drug": drug_id_to_name[d1_id],
                                        "to_drug": drug_id_to_name[d2_id],
                                        "interaction_type": edge_attrs.get("interaction_type", ""),
                                        "severity": edge_attrs.get("severity", ""),
                                    })
                except Exception as edge_err:
                    logger.warning("Failed to fetch drug interactions for %s: %s", patient_id, edge_err)
            result["drug_interactions"] = drug_interactions

            return result
        except Exception as e:
            logger.error("get_patient failed for %s: %s", patient_id, e)
            raise HTTPException(status_code=500, detail="Failed to fetch patient data")

    def upsert_patient(self, patient: dict) -> dict:
        if not self.conn:
            if _db_unavailable():
                return patient
        try:
            self.conn.upsertVertex(
                "Patient",
                patient["patient_id"],
                attributes={k: v for k, v in patient.items() if k != "patient_id"}
            )
            return patient
        except Exception as e:
            logger.error("upsert_patient failed for %s: %s", patient.get("patient_id"), e)
            raise HTTPException(status_code=500, detail="Failed to save patient data")

    # ─── Mock data (dev fallback when USE_MOCK_DATA=true) ────────────────────────

    def _mock_diagnose(self, symptoms):
        return [{"results": [
            {"disease_id": "D001", "name": "Common Cold", "icd10_code": "J00", "severity": "mild",
             "category": "Respiratory", "description": "Viral upper respiratory infection",
             "@direct_score": 4.5, "@indirect_score": 0.0, "@match_count": 2, "@matched_symptoms": {},
             "@affected_systems": ["Respiratory"]},
            {"disease_id": "D002", "name": "Influenza", "icd10_code": "J10", "severity": "moderate",
             "category": "Respiratory", "description": "Seasonal flu",
             "@direct_score": 3.2, "@indirect_score": 0.0, "@match_count": 2, "@matched_symptoms": {},
             "@affected_systems": ["Respiratory"]},
        ]}]

    def _mock_interactions(self, drug_names):
        mock_drugs = [
            {"drug_id": f"DR{i+1:03d}", "name": name, "drug_class": "NSAID", "approval_status": "approved",
             "generic_name": name}
            for i, name in enumerate(drug_names)
        ]
        return [{"all_input": mock_drugs, "@@interaction_edges": []}]

    def _mock_stats(self):
        return {
            "@@disease_count": 5247, "@@symptom_count": 10392, "@@drug_count": 3018,
            "@@side_effect_count": 1784, "@@gene_count": 512, "@@patient_count": 100,
            "@@body_system_count": 13, "@@medical_test_count": 284,
            "@@biomarker_count": 196, "@@risk_factor_count": 87,
            "@@pathway_count": 342, "@@drug_class_count": 48, "@@procedure_count": 213,
            "@@has_symptom_count": 48291, "@@treats_count": 9814,
            "@@interacts_count": 4203, "@@associated_count": 2917, "@@comorbid_count": 3156,
        }

    def _mock_patient_risk(self, patient_id):
        return [{"risk_score": 0.35, "risk_factors": ["Hypertension", "Age > 40"],
                 "high_risk_drugs": [], "recommendations": ["Regular BP monitoring"]}]

    def _mock_pgx(self, patient_id):
        return [{"@@high_risk_drugs": [], "@@patient_phenotypes": [],
                 "@@pgx_matrix": {}, "drugs": [], "at_risk_genes": [],
                 "patient_variants": []}]

    def _mock_progression(self, patient_id):
        return [{"active_diseases": [], "all_stages": [],
                 "@@risk_summary": {}, "@@critical_chains": []}]

    def _mock_comorbidity(self, disease_id):
        return [{"start": [], "cluster": [], "cluster_risk_factors": [],
                 "cluster_systems": [], "cluster_drugs": [], "@@top_comorbidities": {}}]

    def _mock_safety_check(self, patient_id):
        return [{"@@critical_count": 0, "@@major_count": 0,
                 "@@critical_alerts": [], "@@major_alerts": [],
                 "@@moderate_alerts": [], "@@info_alerts": []}]

    def _mock_symptoms(self):
        return [
            {"v_id": "S001", "attributes": {"name": "Fever", "body_system": "General", "severity_weight": 0.8}},
            {"v_id": "S002", "attributes": {"name": "Cough", "body_system": "Respiratory", "severity_weight": 0.6}},
            {"v_id": "S003", "attributes": {"name": "Headache", "body_system": "Neurological", "severity_weight": 0.5}},
            {"v_id": "S004", "attributes": {"name": "Fatigue", "body_system": "General", "severity_weight": 0.4}},
            {"v_id": "S005", "attributes": {"name": "Nausea", "body_system": "Gastrointestinal", "severity_weight": 0.5}},
            {"v_id": "S006", "attributes": {"name": "Chest Pain", "body_system": "Cardiovascular", "severity_weight": 0.9}},
            {"v_id": "S007", "attributes": {"name": "Shortness of Breath", "body_system": "Respiratory", "severity_weight": 0.85}},
            {"v_id": "S008", "attributes": {"name": "Sore Throat", "body_system": "Respiratory", "severity_weight": 0.4}},
        ]

    def _mock_drugs(self):
        return [
            {"v_id": "DR001", "attributes": {"name": "Aspirin", "drug_class": "NSAID", "approval_status": "approved", "generic_name": "Acetylsalicylic acid"}},
            {"v_id": "DR002", "attributes": {"name": "Ibuprofen", "drug_class": "NSAID", "approval_status": "approved", "generic_name": "Ibuprofen"}},
            {"v_id": "DR003", "attributes": {"name": "Warfarin", "drug_class": "Anticoagulant", "approval_status": "approved", "generic_name": "Warfarin sodium"}},
            {"v_id": "DR004", "attributes": {"name": "Metformin", "drug_class": "Biguanide", "approval_status": "approved", "generic_name": "Metformin HCl"}},
            {"v_id": "DR005", "attributes": {"name": "Lisinopril", "drug_class": "ACE inhibitor", "approval_status": "approved", "generic_name": "Lisinopril"}},
        ]
