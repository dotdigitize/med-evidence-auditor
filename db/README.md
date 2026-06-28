# MedEvidence Auditor Demo SQL Database

The SQL files define a MariaDB-ready evidence audit database named `medevidence_demo`.

The application does not require MariaDB for local tests or frontend builds. Set `ENABLE_DATABASE=true` only after MariaDB is installed and configured.

```sql
CREATE DATABASE medevidence_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'medevidence_user'@'localhost' IDENTIFIED BY 'change_this_password';
GRANT ALL PRIVILEGES ON medevidence_demo.* TO 'medevidence_user'@'localhost';
```

```bash
mysql -u medevidence_user -p medevidence_demo < db/schema.sql
mysql -u medevidence_user -p medevidence_demo < db/seed_evidence_demo.sql
```
