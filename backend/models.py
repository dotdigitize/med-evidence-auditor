from pydantic import BaseModel, Field
from typing import Any, Literal

SupportStatus = Literal["supported", "partially_supported", "unsupported", "contradicted", "needs_human_review"]


class AuditProject(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    domain_area: str | None = None


class EvidenceItem(BaseModel):
    id: int | None = None
    project_id: int = 1
    evidence_label: str | None = None
    evidence_text: str
    evidence_type: str | None = None
    source_reference: str | None = None
    confidence_score: float | None = None
    metadata_json: dict[str, Any] | None = None


class ModelOutput(BaseModel):
    id: int | None = None
    project_id: int = 1
    output_title: str = "MAMMAL output"
    model_name: str | None = None
    output_text: str
    output_type: str | None = None
    metadata_json: dict[str, Any] | None = None


class ExtractedClaim(BaseModel):
    id: int | None = None
    model_output_id: int | None = None
    claim_text: str
    claim_type: str = "biomedical_statement"
    medical_risk_level: str = "review"
    support_status: SupportStatus = "needs_human_review"
    support_score: float | None = None
    matched_evidence: list[EvidenceItem] = Field(default_factory=list)
    human_review_status: str = "pending"
    source_fields: dict[str, Any] | None = None


class RiskFlag(BaseModel):
    id: int | None = None
    claim_id: int | None = None
    model_output_id: int | None = None
    flag_type: str
    severity: str
    flag_text: str
    recommendation: str


class AuditRunRequest(BaseModel):
    project_id: int = 1
    model_output: ModelOutput
    evidence_items: list[EvidenceItem] | None = None


class AuditRunResult(BaseModel):
    id: int = 1
    project_id: int
    model_output: ModelOutput
    claims: list[ExtractedClaim]
    risk_flags: list[RiskFlag]
    supported_count: int
    unsupported_count: int


class ClaimExtractionRequest(BaseModel):
    text: str


class MammalImportRequest(BaseModel):
    project_id: int = 1
    import_title: str = "MAMMAL output import"
    raw_json: dict[str, Any] | None = None
    raw_text: str | None = None


class ReportExportRequest(BaseModel):
    format: Literal["markdown", "json", "both"] = "both"
