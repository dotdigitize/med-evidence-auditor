# MedEvidence Auditor Setup

Created by Jose Perez.

## 1. Build and test without MariaDB, Ollama, or MAMMAL
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
npm install
npm run build
```

Default local settings keep external services disabled.

## 2. Optional MariaDB setup for later deployment
```bash
sudo apt install mariadb-server mariadb-client
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

Set `ENABLE_DATABASE=true` only after the database is available.

## 3. Optional Ollama setup for local LLM audit
```bash
ollama pull gemma4:e4b
ollama pull gemma4:e2b
```

Set `ENABLE_LLM_AUDIT=true` only after Ollama is available.

## 4. MAMMAL output import usage
Set `ENABLE_MAMMAL_IMPORT=true` for the default MAMMAL import workflow. The parser accepts saved MAMMAL JSON or text biomedical output and converts it into an audit-ready MAMMAL output record.

Live MAMMAL command execution remains disabled unless explicitly configured:

```env
MAMMAL_COMMAND_ENABLED=false
MAMMAL_COMMAND=
```
