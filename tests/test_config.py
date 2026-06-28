from backend.config import get_settings


def test_default_config_disables_external_services():
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.app_name == "MedEvidence Auditor"
    assert settings.db_name == "medevidence_demo"
    assert settings.db_user == "medevidence_user"
    assert settings.enable_database is False
    assert settings.enable_llm_audit is False
    assert settings.enable_mammal_import is True
    assert settings.mammal_command_enabled is False
    assert settings.mammal_command == ""
