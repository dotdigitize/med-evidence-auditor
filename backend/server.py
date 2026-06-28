from fastapi import FastAPI, HTTPException
from backend.audit_store import store
from backend.claim_extractor import extract_claims
from backend.config import get_settings
from backend.mammal_importer import parse_mammal_output
from backend.models import AuditProject, AuditRunRequest, ClaimExtractionRequest, EvidenceItem, MammalImportRequest, ModelOutput, ReportExportRequest
from backend.reporting import export_audit_report
from backend.sample_data import load_sample_evidence, load_sample_model_output, load_sample_project, sample_overview

app = FastAPI(title="MedEvidence Auditor", version="0.1.0")


@app.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "app": settings.app_name,
        "status": "ok",
        "database_enabled": settings.enable_database,
        "llm_audit_enabled": settings.enable_llm_audit,
        "mammal_import_enabled": settings.enable_mammal_import,
    }


@app.get("/api/system/status")
def system_status() -> dict:
    settings = get_settings()
    return {
        "database": "configured" if settings.enable_database else "disabled",
        "local_llm_audit": "configured" if settings.enable_llm_audit else "disabled",
        "mammal_import": "configured" if settings.enable_mammal_import else "disabled",
        "local_development_mode": not settings.enable_database,
    }


@app.get("/api/projects")
def get_projects() -> list[AuditProject]:
    return [load_sample_project()]


@app.post("/api/projects")
def create_project(project: AuditProject) -> AuditProject:
    project.id = project.id or 1
    return project


@app.get("/api/evidence")
def get_evidence() -> list[EvidenceItem]:
    return load_sample_evidence()


@app.post("/api/evidence")
def create_evidence(item: EvidenceItem) -> EvidenceItem:
    item.id = item.id or 1
    return item


@app.get("/api/model-outputs")
def get_model_outputs() -> list[ModelOutput]:
    return [load_sample_model_output()]


@app.post("/api/model-outputs")
def create_model_output(output: ModelOutput) -> ModelOutput:
    output.id = output.id or 1
    return output


@app.post("/api/audits/run")
def run_audit(request: AuditRunRequest):
    return store.run_audit(request)


@app.get("/api/audits")
def get_audits():
    return store.list_audits()


@app.get("/api/audits/{audit_id}")
def get_audit(audit_id: int):
    audit = store.get_audit(audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit


@app.get("/api/audits/{audit_id}/claims")
def get_audit_claims(audit_id: int):
    audit = get_audit(audit_id)
    return audit.claims


@app.get("/api/audits/{audit_id}/risk-flags")
def get_audit_risk_flags(audit_id: int):
    audit = get_audit(audit_id)
    return audit.risk_flags


@app.post("/api/claims/extract")
def extract_claim_endpoint(request: ClaimExtractionRequest):
    return {"claims": extract_claims(request.text)}


@app.post("/api/claims/{claim_id}/review")
def review_claim(claim_id: int, payload: dict):
    return {"claim_id": claim_id, "review_status": payload.get("review_status", "reviewed"), "note": payload.get("note")}


@app.post("/api/mammal/import")
def mammal_import(request: MammalImportRequest):
    return parse_mammal_output(request)


@app.post("/api/reports/{audit_id}/export")
def export_report(audit_id: int, request: ReportExportRequest):
    audit = get_audit(audit_id)
    paths = export_audit_report(audit)
    return {"audit_id": audit_id, "format": request.format, "files": paths}


@app.get("/api/sample/overview")
def sample():
    return sample_overview()
