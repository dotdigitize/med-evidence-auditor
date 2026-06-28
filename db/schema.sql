CREATE TABLE IF NOT EXISTS audit_projects (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(190) NOT NULL,
  description TEXT,
  domain_area VARCHAR(190),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS source_documents (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  project_id BIGINT NOT NULL,
  title VARCHAR(255) NOT NULL,
  source_type VARCHAR(120),
  source_reference TEXT,
  content_text MEDIUMTEXT,
  metadata_json JSON NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_source_documents_project (project_id),
  CONSTRAINT fk_source_documents_project FOREIGN KEY (project_id) REFERENCES audit_projects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS evidence_items (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  project_id BIGINT NOT NULL,
  source_document_id BIGINT NULL,
  evidence_label VARCHAR(255),
  evidence_text MEDIUMTEXT NOT NULL,
  evidence_type VARCHAR(120),
  source_reference TEXT,
  confidence_score DECIMAL(10,5) NULL,
  metadata_json JSON NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_evidence_project (project_id),
  INDEX idx_evidence_source_document (source_document_id),
  CONSTRAINT fk_evidence_project FOREIGN KEY (project_id) REFERENCES audit_projects(id) ON DELETE CASCADE,
  CONSTRAINT fk_evidence_source_document FOREIGN KEY (source_document_id) REFERENCES source_documents(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS model_outputs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  project_id BIGINT NOT NULL,
  output_title VARCHAR(255) NOT NULL,
  model_name VARCHAR(190),
  output_text MEDIUMTEXT NOT NULL,
  output_type VARCHAR(120),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_model_outputs_project (project_id),
  CONSTRAINT fk_model_outputs_project FOREIGN KEY (project_id) REFERENCES audit_projects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS extracted_claims (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  model_output_id BIGINT NOT NULL,
  claim_text MEDIUMTEXT NOT NULL,
  claim_type VARCHAR(120),
  medical_risk_level VARCHAR(80),
  support_status VARCHAR(80) DEFAULT 'needs_review',
  support_score DECIMAL(10,5) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_claims_model_output (model_output_id),
  INDEX idx_claims_support_status (support_status),
  CONSTRAINT fk_claims_model_output FOREIGN KEY (model_output_id) REFERENCES model_outputs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS claim_evidence_links (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  claim_id BIGINT NOT NULL,
  evidence_item_id BIGINT NOT NULL,
  match_score DECIMAL(10,5) NULL,
  relationship_type VARCHAR(120),
  review_note TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_claim_links_claim (claim_id),
  INDEX idx_claim_links_evidence (evidence_item_id),
  CONSTRAINT fk_claim_links_claim FOREIGN KEY (claim_id) REFERENCES extracted_claims(id) ON DELETE CASCADE,
  CONSTRAINT fk_claim_links_evidence FOREIGN KEY (evidence_item_id) REFERENCES evidence_items(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS risk_flags (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  claim_id BIGINT NULL,
  model_output_id BIGINT NULL,
  flag_type VARCHAR(120) NOT NULL,
  severity VARCHAR(80) NOT NULL,
  flag_text TEXT,
  recommendation TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_risk_flags_claim (claim_id),
  INDEX idx_risk_flags_model_output (model_output_id),
  INDEX idx_risk_flags_type (flag_type),
  CONSTRAINT fk_risk_flags_claim FOREIGN KEY (claim_id) REFERENCES extracted_claims(id) ON DELETE SET NULL,
  CONSTRAINT fk_risk_flags_model_output FOREIGN KEY (model_output_id) REFERENCES model_outputs(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS audit_runs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  project_id BIGINT NOT NULL,
  model_output_id BIGINT NOT NULL,
  run_status VARCHAR(80) DEFAULT 'Created',
  claims_count INT DEFAULT 0,
  supported_count INT DEFAULT 0,
  unsupported_count INT DEFAULT 0,
  risk_flags_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_audit_runs_project (project_id),
  INDEX idx_audit_runs_model_output (model_output_id),
  CONSTRAINT fk_audit_runs_project FOREIGN KEY (project_id) REFERENCES audit_projects(id) ON DELETE CASCADE,
  CONSTRAINT fk_audit_runs_model_output FOREIGN KEY (model_output_id) REFERENCES model_outputs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS audit_reports (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  audit_run_id BIGINT NOT NULL,
  report_format VARCHAR(80) NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_audit_reports_run (audit_run_id),
  CONSTRAINT fk_audit_reports_run FOREIGN KEY (audit_run_id) REFERENCES audit_runs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mammal_imports (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  project_id BIGINT NOT NULL,
  import_title VARCHAR(255) NOT NULL,
  raw_json JSON NULL,
  raw_text MEDIUMTEXT NULL,
  parsed_summary TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_mammal_imports_project (project_id),
  CONSTRAINT fk_mammal_imports_project FOREIGN KEY (project_id) REFERENCES audit_projects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS audit_events (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  entity_type VARCHAR(120),
  entity_id BIGINT NULL,
  event_type VARCHAR(120) NOT NULL,
  event_note TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_audit_events_entity (entity_type, entity_id),
  INDEX idx_audit_events_type (event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
