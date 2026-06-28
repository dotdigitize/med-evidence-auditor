# MedEvidence Auditor

<img width="1916" height="821" alt="jose perez agi engineer MedEvidence Auditor" src="https://github.com/user-attachments/assets/54956066-9604-4916-b0e3-ce8412d344be" />

MedEvidence Auditor is an open source MAMMAL evidence auditing system for reviewing MAMMAL biomedical model outputs, extracting claims, matching claims to supporting evidence, flagging weak or unsupported statements, detecting risky medical language, and exporting structured verification reports.

Created by Jose Perez.

## Overview
MedEvidence Auditor turns MAMMAL output into a traceable audit trail: model claim, evidence, support score, source reference, uncertainty note, risk flag, and human review status.

Core workflow:

```text

MAMMAL output -> MAMMAL output parser -> MAMMAL claim extraction -> evidence matching -> support scoring -> risk flagging -> human review status -> Markdown/JSON audit report
```

## Why MedEvidence Auditor Exists
MAMMAL and other biomedical AI systems can generate outputs that sound confident but may be incomplete, unsupported, overstated, or missing uncertainty. This project helps researchers, developers, and medical operations teams review MAMMAL-generated biomedical statements before they are trusted.

## Core Features
- MAMMAL output import and parsing.
- MAMMAL claim extraction.
- MAMMAL evidence matching.
- Risk flagging for biomedical and medical language.
- Audit projects, evidence items, MAMMAL outputs, extracted claims, risk flags, and reports.
- Deterministic local claim extraction and evidence matching.
- Markdown and JSON verification reports.
- MariaDB-ready schema without requiring MariaDB for local tests.
- Optional Ollama-compatible local LLM audit layer for deeper explanation.

## Architecture
The backend uses Python, FastAPI, Pydantic, mysql-connector-python, and deterministic MAMMAL audit modules. The frontend uses React, TypeScript, Vite, and Tailwind CSS 3. The database design targets MariaDB and avoids SQLite.

Required backend modules:

- `backend/mammal_importer.py`
- `backend/mammal_output_parser.py`
- `backend/mammal_claim_extractor.py`
- `backend/evidence_matcher.py`
- `backend/risk_flagger.py`
- `backend/reporting.py`

## MAMMAL Output Import and Audit Pipeline
The MAMMAL output import and audit pipeline accepts MAMMAL JSON or text biomedical model output and converts it into an audit-ready record. The parser extracts candidate markers, pathway notes, model findings, summary statements, scores, confidence notes, and biomedical claims. Those claims are then matched against evidence items and scored for support.

Running a live MAMMAL command is not required. Importing and parsing saved MAMMAL output is the default workflow. Generic biomedical AI text can be reviewed as a secondary input path, but MedEvidence Auditor is designed around MAMMAL output auditing.

## Claim Extraction
MAMMAL claim extraction converts parsed MAMMAL output into audit claims. It includes marker claims, pathway claims, summary claims, and finding claims while preserving source fields from the original parsed output.

## Evidence Matching
Evidence matching uses normalized lexical overlap, phrase overlap, support scoring, and support status classification: supported, partially supported, unsupported, contradicted, or needs human review.

## Risk Flagging
Risk flagging detects diagnosis claims, treatment recommendations, individual risk prediction, overconfident conclusions, missing uncertainty, missing source evidence, unsupported causal claims, and clinical action language.

## MAMMAL Audit Examples
MedEvidence Auditor is built around one primary workflow:

```text
MAMMAL output -> claim extraction -> evidence matching -> risk flagging -> human review -> audit report
```

The system does not treat MAMMAL output as the final answer. It treats MAMMAL output as biomedical model output that must be reviewed, scored, and traced before it is trusted.

### Example 1: Candidate Marker Support Audit
MAMMAL output

```json
{
  "run_id": "mammal_scz_001",
  "finding": "IL6 and TNF-related inflammatory markers show increased relevance in the schizophrenia research signal set.",
  "candidate_markers": [
    {"name": "IL6", "type": "gene", "score": 0.82, "direction": "increased"},
    {"name": "TNF", "type": "gene", "score": 0.77, "direction": "increased"}
  ],
  "pathway_notes": ["neuroinflammation", "immune activation"]
}
```

Evidence supplied:

```text
The synthetic research fixture contains neuroinflammation notes referencing IL6, TNF, cytokine activity, and immune signaling as research-level markers associated with schizophrenia-related literature review themes.
```

Audit result:

```text
Claim: IL6 and TNF-related inflammatory markers show increased relevance.
Support status: supported
Support score: 0.84
Matched evidence: neuroinflammation notes, cytokine activity references, immune signaling references
Risk flags: none
Human review status: review recommended before publication
```

### Example 2: Unsupported Causal Claim Detection
MAMMAL output

```text
The dopamine pathway markers prove schizophrenia progression in this dataset.
```

Evidence supplied:

```text
The available evidence mentions dopamine pathway involvement as a research theme, but does not establish proof, progression, or causal certainty.
```

Audit result:

```text
Claim: Dopamine pathway markers prove schizophrenia progression.
Support status: unsupported
Support score: 0.31
Risk flags:
- unsupported_causal_claim
- overconfident_language
- missing_uncertainty

Recommendation:
Rewrite as a research-level association, not a proof claim.
```

### Example 3: Treatment Recommendation Risk Flag
MAMMAL output

```text
The marker pattern indicates that glutamate-targeting treatment should be used.
```

Evidence supplied:

```text
The evidence library contains research notes about glutamate signaling and synaptic pathway involvement, but no clinical treatment protocol, patient-specific evaluation, or therapeutic recommendation evidence.
```

Audit result:

```text
Claim: Glutamate-targeting treatment should be used.
Support status: needs_human_review
Support score: 0.28
Risk flags:
- treatment_recommendation
- clinical_action_language
- missing_evidence

Recommendation:
Remove treatment language. Keep the statement at the research interpretation level.
```

### Example 4: MAMMAL Pathway Summary Audit
MAMMAL output

```json
{
  "summary": "Synaptic signaling, glutamate activity, and immune activation appear as candidate pathway clusters in the schizophrenia research run.",
  "pathways": [
    {"name": "synaptic signaling", "score": 0.79},
    {"name": "glutamate activity", "score": 0.74},
    {"name": "immune activation", "score": 0.71}
  ]
}
```

Audit result:

```text
Extracted claims:
1. Synaptic signaling appears as a candidate pathway cluster.
2. Glutamate activity appears as a candidate pathway cluster.
3. Immune activation appears as a candidate pathway cluster.

Support statuses:
1. partially_supported
2. partially_supported
3. supported

Risk flags:
- missing_uncertainty for claims without confidence context

Report output:
reports/latest_audit_report.md
reports/latest_audit_report.json
```

### Example 5: Full MAMMAL Evidence Audit Report
A complete audit report includes:

```text
Audit Summary
MAMMAL Output Reviewed
Extracted MAMMAL Claims
Evidence Support Table
Unsupported Claims
Risk Flags
Human Review Notes
Medical Safety Notice
Next Review Steps
```

The goal is to make every MAMMAL finding traceable:

```text
MAMMAL claim
-> matched evidence
-> support score
-> risk flags
-> source reference
-> human review status
-> exportable report
```

## Medical Safety Notice
This is not a diagnostic system.
It does not diagnose, treat, prescribe, predict individual medical risk, or replace licensed clinical judgment.
It is a MAMMAL evidence review and research safety layer.

## Local LLM Audit Layer
When `ENABLE_LLM_AUDIT=true`, the backend can call an Ollama-compatible local model for deeper audit explanation. If Ollama is unavailable, the deterministic extractor remains available.

## MariaDB Evidence Database
Production deployment design uses MariaDB with parameterized SQL only. No raw SQL execution endpoint is included.

## Demo SQL Database
SQL files in `db/` create and seed `medevidence_demo` for later deployment:
- `db/schema.sql`
- `db/seed_evidence_demo.sql`
- `db/reset_demo_database.sql`

## Sample Evidence Fixtures
`sample_data/` contains synthetic schizophrenia research fixtures for local development. These fixtures include gene expression signal notes, neuroinflammation notes, synaptic pathway candidate markers, dopamine/glutamate pathway notes, polygenic risk discussion, and MAMMAL synthetic output. They contain no patient identifiers.

## Audit Reports
Reports export to `REPORT_OUTPUT_DIR` as:
- `reports/latest_audit_report.md`
- `reports/latest_audit_report.json`

## Local Development Without MariaDB, Ollama, or MAMMAL
The default `.env.example` sets `ENABLE_DATABASE=false`, `ENABLE_LLM_AUDIT=false`, and `ENABLE_MAMMAL_IMPORT=true`. In this mode, the API uses sample evidence fixtures, imports saved MAMMAL output, and does not require external services.

Live MAMMAL command execution is disabled by default:

```env
MAMMAL_COMMAND_ENABLED=false
MAMMAL_COMMAND=
```

## Optional MariaDB Setup for Deployment
```bash
sudo apt install mariadb-server mariadb-client
mysql -u root -p
```

```sql
CREATE DATABASE medevidence_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'medevidence_user'@'localhost' IDENTIFIED BY 'change_this_password';
GRANT ALL PRIVILEGES ON medevidence_demo.* TO 'medevidence_user'@'localhost';
```

```bash
mysql -u medevidence_user -p medevidence_demo < db/schema.sql
mysql -u medevidence_user -p medevidence_demo < db/seed_evidence_demo.sql
```

## Optional Ollama Setup
```bash
ollama pull gemma4:e4b
ollama pull gemma4:e2b
```

Set `ENABLE_LLM_AUDIT=true` only after Ollama is available.

## Backend Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.server:app --reload
```

## Frontend Setup
```bash
npm install
npm run build
npm run dev
```

## Running Tests
```bash
python -m pytest
```

## API Overview
Endpoints include `/health`, `/api/system/status`, `/api/projects`, `/api/evidence`, `/api/model-outputs`, `/api/audits/run`, `/api/audits`, `/api/claims/extract`, `/api/mammal/import`, `/api/reports/{audit_id}/export`, and `/api/sample/overview`.

## Security Notes
No authentication is included for local development. Add authentication, authorization, HTTPS, access controls, audit logging, backup policies, and secret management before public deployment.

## Privacy Notes
No cloud APIs are required. Data remains local unless users configure external services. Users are responsible for privacy, consent, retention, deletion, backup encryption, and compliance when using real datasets.

## Project Structure
`backend/` contains FastAPI and MAMMAL audit logic. `frontend/` contains the React dashboard. `db/` contains MariaDB SQL. `sample_data/` contains synthetic research fixtures. `tests/` contains local tests.

## License
Apache License 2.0. Copyright 2026 Jose Perez.

## Attribution
MedEvidence Auditor was created by Jose Perez. Preserve copyright notices, license notices, and attribution to Jose Perez as the original creator when redistributing or modifying this software.
