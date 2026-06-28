INSERT INTO audit_projects (id, name, description, domain_area)
VALUES (1, 'Schizophrenia Research Evidence Audit', 'Synthetic research fixture for auditing MAMMAL biomedical statements against curated evidence notes.', 'schizophrenia research operations')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO source_documents (id, project_id, title, source_type, source_reference, content_text)
VALUES
  (1, 1, 'Synthetic Gene Expression Signal Notes', 'research_fixture', 'sample-fixture:gene-expression', 'Curated synthetic notes describe gene expression signals observed at the research cohort level with uncertainty limits.'),
  (2, 1, 'Synthetic Neuroinflammation Evidence Notes', 'research_fixture', 'sample-fixture:neuroinflammation', 'Curated synthetic notes describe inflammatory pathway markers in aggregate schizophrenia research summaries.')
ON DUPLICATE KEY UPDATE title = VALUES(title);

INSERT INTO evidence_items (id, project_id, source_document_id, evidence_label, evidence_text, evidence_type, source_reference, confidence_score)
VALUES
  (1, 1, 1, 'Gene expression signal note', 'Aggregate schizophrenia research notes suggest altered gene expression signals may be associated with synaptic pathway markers. The notes do not establish diagnosis or treatment response.', 'synthetic research fixture', 'sample-fixture:gene-expression', 0.72000),
  (2, 1, 2, 'Neuroinflammation evidence note', 'Synthetic neuroinflammation evidence notes describe increased inflammation pathway markers in research summaries, with uncertainty about causality and clinical interpretation.', 'synthetic research fixture', 'sample-fixture:neuroinflammation', 0.68000),
  (3, 1, NULL, 'Dopamine and glutamate pathway note', 'Dopamine and glutamate pathway research notes describe candidate marker associations at population research level. They do not predict individual risk.', 'synthetic research fixture', 'sample-fixture:neurotransmitter-pathways', 0.70000),
  (4, 1, NULL, 'Polygenic research discussion', 'Polygenic risk discussion is limited to research-level association and should not be used for individual diagnosis, treatment, or patient risk prediction.', 'synthetic research fixture', 'sample-fixture:polygenic-risk', 0.66000)
ON DUPLICATE KEY UPDATE evidence_label = VALUES(evidence_label);

INSERT INTO model_outputs (id, project_id, output_title, model_name, output_text, output_type)
VALUES (1, 1, 'Synthetic schizophrenia MAMMAL output', 'MAMMAL', 'Gene expression markers may be associated with altered synaptic pathway activity in schizophrenia research summaries.\nMAMMAL output states increased inflammation pathway signals could explain a subset of research cohort observations.\nDopamine and glutamate pathway markers are candidate markers and should remain bounded by source uncertainty.\nPolygenic risk proves individual diagnosis and will diagnose future schizophrenia.\nThis MAMMAL output recommends treatment based on the marker panel.', 'mammal_text')
ON DUPLICATE KEY UPDATE output_title = VALUES(output_title);
