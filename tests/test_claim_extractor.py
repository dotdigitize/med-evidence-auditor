from backend.claim_extractor import extract_claims


def test_extract_claims_uses_biomedical_signal_words():
    text = "Short note. Dopamine pathway markers may be associated with response in research summaries. Weather is clear."
    claims = extract_claims(text)
    assert len(claims) == 1
    assert "Dopamine pathway" in claims[0].claim_text
    assert claims[0].claim_type in {"biomedical_mechanism", "clinical_or_risk_statement"}
