from backend.models import ExtractedClaim
from backend.risk_flagger import flag_claim_risks


def test_risk_flagger_detects_medical_safety_risks():
    claim = ExtractedClaim(id=1, claim_text="Polygenic risk proves individual diagnosis and will diagnose future schizophrenia.", support_status="unsupported")
    flags = flag_claim_risks(claim)
    flag_types = {flag.flag_type for flag in flags}
    assert "diagnosis_claim" in flag_types
    assert "overconfident_language" in flag_types
    assert "missing_evidence" in flag_types
