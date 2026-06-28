import json
from pathlib import Path
from backend.config import get_settings
from backend.models import AuditRunResult

SAFETY_NOTICE = (
    "This is not a diagnostic system. It does not diagnose, treat, prescribe, predict individual medical "
    "risk, or replace licensed clinical judgment. It is a MAMMAL evidence review and research safety layer."
)


def audit_to_dict(result: AuditRunResult) -> dict:
    return result.model_dump()


def render_markdown_report(result: AuditRunResult) -> str:
    lines = [
        "# MAMMAL Evidence Audit Report",
        "",
        "## Audit Summary",
        f"- Claims reviewed: {len(result.claims)}",
        f"- Supported claims: {result.supported_count}",
        f"- Unsupported claims: {result.unsupported_count}",
        f"- Risk flags: {len(result.risk_flags)}",
        "",
        "## MAMMAL Output Reviewed",
        result.model_output.output_text,
        "",
        "## Extracted MAMMAL Claims",
    ]
    for claim in result.claims:
        lines.append(f"- {claim.claim_text}")
    lines.extend(["", "## Evidence Support Table", "| Claim | Support | Score | Evidence |", "| --- | --- | ---: | --- |"])
    for claim in result.claims:
        evidence = claim.matched_evidence[0].evidence_label if claim.matched_evidence else "Needs source review"
        lines.append(f"| {claim.claim_text} | {claim.support_status} | {claim.support_score or 0:.2f} | {evidence} |")
    lines.extend(["", "## Unsupported Claims"])
    for claim in result.claims:
        if claim.support_status in {"unsupported", "needs_human_review", "contradicted"}:
            lines.append(f"- {claim.claim_text}")
    lines.extend(["", "## Risk Flags"])
    for flag in result.risk_flags:
        lines.append(f"- **{flag.flag_type} ({flag.severity})**: {flag.recommendation}")
    lines.extend([
        "",
        "## Human Review Notes",
        "Claims marked as unsupported, contradicted, or needing human review require qualified domain review.",
        "",
        "## Medical Safety Notice",
        SAFETY_NOTICE,
        "",
        "## Next Review Steps",
        "Confirm source references, add missing uncertainty, and document reviewer disposition before operational use.",
    ])
    return "\n".join(lines) + "\n"


def export_audit_report(result: AuditRunResult, output_dir: Path | None = None) -> dict[str, str]:
    output_dir = output_dir or get_settings().report_output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "latest_audit_report.md"
    json_path = output_dir / "latest_audit_report.json"
    md_path.write_text(render_markdown_report(result))
    json_path.write_text(json.dumps(audit_to_dict(result), indent=2))
    return {"markdown": str(md_path), "json": str(json_path)}
