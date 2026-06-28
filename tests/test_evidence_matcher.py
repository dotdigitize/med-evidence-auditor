from backend.evidence_matcher import classify_support_status, phrase_overlap_score, support_score, token_overlap_score


def test_support_scoring_and_classification():
    claim = "Dopamine and glutamate pathway markers are candidate research markers."
    evidence = "Dopamine and glutamate pathway research notes describe candidate marker associations."
    assert token_overlap_score(claim, evidence) > 0.4
    assert phrase_overlap_score(claim, evidence) > 0.1
    score = support_score(claim, evidence)
    assert score > 0.45
    assert classify_support_status(score, claim, evidence) in {"supported", "partially_supported"}
