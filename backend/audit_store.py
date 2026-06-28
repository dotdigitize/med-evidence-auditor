from backend.claim_extractor import extract_claims
from backend.evidence_matcher import match_claims
from backend.mammal_claim_extractor import extract_mammal_claims
from backend.models import AuditRunRequest, AuditRunResult
from backend.risk_flagger import flag_risks
from backend.sample_data import load_sample_evidence


class InMemoryAuditStore:
    def __init__(self) -> None:
        self.audit_runs: dict[int, AuditRunResult] = {}
        self.next_id = 1

    def run_audit(self, request: AuditRunRequest) -> AuditRunResult:
        evidence = request.evidence_items or load_sample_evidence()
        mammal_parsed = (request.model_output.metadata_json or {}).get("mammal_parsed")
        claims = extract_mammal_claims(mammal_parsed) if mammal_parsed else extract_claims(request.model_output.output_text)
        for idx, claim in enumerate(claims, start=1):
            claim.id = idx
            claim.model_output_id = request.model_output.id
        matched = match_claims(claims, evidence)
        flags = flag_risks(matched)
        result = AuditRunResult(
            id=self.next_id,
            project_id=request.project_id,
            model_output=request.model_output,
            claims=matched,
            risk_flags=flags,
            supported_count=sum(1 for claim in matched if claim.support_status == "supported"),
            unsupported_count=sum(1 for claim in matched if claim.support_status in {"unsupported", "contradicted", "needs_human_review"}),
        )
        self.audit_runs[result.id] = result
        self.next_id += 1
        return result

    def list_audits(self) -> list[AuditRunResult]:
        return list(self.audit_runs.values())

    def get_audit(self, audit_id: int) -> AuditRunResult | None:
        return self.audit_runs.get(audit_id)


store = InMemoryAuditStore()
