# Architecture

MedEvidence Auditor was created by Jose Perez.

The system has four layers:

- FastAPI backend for project, evidence, MAMMAL output, audit, claim, risk flag, MAMMAL import, and report endpoints.
- Deterministic MAMMAL audit engine for claim extraction, evidence matching, risk flagging, and report rendering.
- MariaDB-ready persistence design using parameterized SQL and SQL files in `db/`.
- React, TypeScript, Vite, and Tailwind CSS dashboard for evidence review workflows.

Local development does not require MariaDB, Ollama, MAMMAL, or external APIs. When `ENABLE_DATABASE=false`, backend endpoints return sample evidence fixture data or in-memory audit results.
