from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()


def _bool(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "MedEvidence Auditor")
    db_host: str = os.getenv("DB_HOST", "127.0.0.1")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_name: str = os.getenv("DB_NAME", "medevidence_demo")
    db_user: str = os.getenv("DB_USER", "medevidence_user")
    db_password: str = os.getenv("DB_PASSWORD", "change_this_password")
    enable_database: bool = _bool("ENABLE_DATABASE")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    claim_model: str = os.getenv("CLAIM_MODEL", "gemma4:e4b")
    critique_model: str = os.getenv("CRITIQUE_MODEL", "gemma4:e2b")
    enable_llm_audit: bool = _bool("ENABLE_LLM_AUDIT")
    enable_mammal_import: bool = _bool("ENABLE_MAMMAL_IMPORT", "true")
    mammal_command_enabled: bool = _bool("MAMMAL_COMMAND_ENABLED")
    mammal_command: str = os.getenv("MAMMAL_COMMAND", "")
    report_output_dir: Path = Path(os.getenv("REPORT_OUTPUT_DIR", "./reports"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
