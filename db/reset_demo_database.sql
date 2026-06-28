DROP TABLE IF EXISTS audit_events;
DROP TABLE IF EXISTS mammal_imports;
DROP TABLE IF EXISTS audit_reports;
DROP TABLE IF EXISTS audit_runs;
DROP TABLE IF EXISTS risk_flags;
DROP TABLE IF EXISTS claim_evidence_links;
DROP TABLE IF EXISTS extracted_claims;
DROP TABLE IF EXISTS model_outputs;
DROP TABLE IF EXISTS evidence_items;
DROP TABLE IF EXISTS source_documents;
DROP TABLE IF EXISTS audit_projects;

SOURCE db/schema.sql;
SOURCE db/seed_evidence_demo.sql;
