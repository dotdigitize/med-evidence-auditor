from backend.sample_data import load_sample_evidence, load_sample_model_output, load_sample_project, sample_overview


def test_sample_data_loads_without_patient_identifiers():
    project = load_sample_project()
    evidence = load_sample_evidence()
    output = load_sample_model_output()
    assert project.name == "Schizophrenia Research Evidence Audit"
    assert len(evidence) >= 4
    assert "patient identifier" not in output.output_text.lower()
    assert sample_overview()["fixture_type"] == "synthetic research fixture"
