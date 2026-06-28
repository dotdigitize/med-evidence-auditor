from backend.models import ExtractedClaim, RiskFlag

OVERCONFIDENT_TERMS = [
    "proves", "guarantees", "will diagnose", "will treat", "definitive",
    "certainly", "always", "never", "cures", "prevents",
]
UNCERTAINTY_TERMS = ["may", "might", "could", "associated", "candidate", "suggests", "limited", "uncertain"]


def _flag(claim: ExtractedClaim, flag_type: str, severity: str, recommendation: str) -> RiskFlag:
    return RiskFlag(
        claim_id=claim.id,
        flag_type=flag_type,
        severity=severity,
        flag_text=claim.claim_text,
        recommendation=recommendation,
    )


def flag_claim_risks(claim: ExtractedClaim) -> list[RiskFlag]:
    text = claim.claim_text.lower()
    flags: list[RiskFlag] = []
    if "diagnosis" in text or "diagnose" in text:
        flags.append(_flag(claim, "diagnosis_claim", "high", "Keep diagnosis language out of automated evidence summaries."))
    if "treatment" in text or "treat" in text or "therapy" in text:
        flags.append(_flag(claim, "treatment_recommendation", "high", "Route treatment statements to qualified clinical review."))
    if "individual risk" in text or "patient risk" in text or "predicts risk" in text:
        flags.append(_flag(claim, "individual_risk_prediction", "high", "Do not infer individual risk from this research audit layer."))
    if any(term in text for term in OVERCONFIDENT_TERMS):
        flags.append(_flag(claim, "overconfident_language", "medium", "Replace certainty with bounded research wording."))
    if not any(term in text for term in UNCERTAINTY_TERMS):
        flags.append(_flag(claim, "missing_uncertainty", "medium", "Add uncertainty language and scope limits."))
    if claim.support_status in {"unsupported", "needs_human_review"}:
        flags.append(_flag(claim, "missing_evidence", "medium", "Attach source evidence or mark for human review."))
    if any(term in text for term in ["causes", "drives", "prove", "proves"]) and claim.support_status != "supported":
        flags.append(_flag(claim, "unsupported_causal_claim", "high", "Do not make causal claims without direct support."))
    if any(term in text for term in ["recommend", "should prescribe", "should be used", "clinical action"]):
        flags.append(_flag(claim, "clinical_action_language", "high", "Remove clinical action language from research operations output."))
    return flags


def flag_risks(claims: list[ExtractedClaim]) -> list[RiskFlag]:
    flags: list[RiskFlag] = []
    for claim in claims:
        flags.extend(flag_claim_risks(claim))
    for idx, flag in enumerate(flags, start=1):
        flag.id = idx
    return flags
