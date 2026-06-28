from backend.mammal_claim_extractor import extract_mammal_claims
from backend.mammal_output_parser import parse_mammal_output


def test_mammal_claim_extractor_includes_marker_pathway_finding_and_summary_claims():
    parsed = parse_mammal_output(
        {
            "run_id": "mammal_scz_002",
            "summary": "Immune activation appears as a candidate pathway cluster.",
            "findings": ["IL6 and TNF inflammatory markers show increased relevance."],
            "candidate_markers": [{"name": "IL6", "type": "gene", "score": 0.82, "direction": "increased"}],
            "pathway_notes": ["neuroinflammation"],
        }
    )

    claims = extract_mammal_claims(parsed)
    claim_text = " ".join(claim.claim_text for claim in claims)

    assert "IL6 increased appears as a candidate biomedical marker" in claim_text
    assert "neuroinflammation appears as a MAMMAL pathway note" in claim_text
    assert "IL6 and TNF inflammatory markers" in claim_text
    assert "Immune activation appears" in claim_text
    assert all(claim.source_fields and claim.source_fields["run_id"] == "mammal_scz_002" for claim in claims)
