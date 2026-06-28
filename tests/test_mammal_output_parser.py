from backend.mammal_output_parser import parse_mammal_output


def test_mammal_output_parser_accepts_json_dictionary():
    parsed = parse_mammal_output(
        {
            "run_id": "mammal_scz_001",
            "finding": "IL6 and TNF inflammatory markers show increased relevance.",
            "candidate_markers": [{"name": "IL6", "type": "gene", "score": 0.82, "direction": "increased"}],
            "pathway_notes": ["neuroinflammation"],
            "summary": "Immune activation appears as a candidate pathway cluster.",
            "confidence_notes": ["Research-level signal only."],
            "confidence_score": 0.74,
        }
    )

    assert parsed["run_id"] == "mammal_scz_001"
    assert parsed["candidate_markers"][0]["name"] == "IL6"
    assert parsed["pathway_notes"] == ["neuroinflammation"]
    assert "IL6" in parsed["findings"][0]
    assert parsed["summary_text"].startswith("Immune activation")
    assert parsed["confidence_notes"] == ["Research-level signal only."]
    assert parsed["scores"]["confidence_score"] == 0.74


def test_mammal_output_parser_accepts_text():
    parsed = parse_mammal_output(
        """run_id: mammal_text_001
        Summary: Dopamine pathway markers remain candidate research markers.
        Candidate marker: TNF score 0.77
        Pathway note: immune activation
        Finding: Glutamate activity appears in the pathway cluster.
        """
    )

    assert parsed["run_id"] == "mammal_text_001"
    assert parsed["candidate_markers"][0]["name"] == "TNF"
    assert parsed["candidate_markers"][0]["score"] == 0.77
    assert "immune activation" in parsed["pathway_notes"][0]
    assert "Glutamate" in parsed["findings"][0]
