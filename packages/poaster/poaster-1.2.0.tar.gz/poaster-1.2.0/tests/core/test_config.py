import logging

import pytest
from uvicorn.logging import TRACE_LOG_LEVEL

from poaster.core.config import LogLevel, Settings, get_log_level, get_settings


def test_get_settings_from_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("LOG_LEVEL", "critical")
    monkeypatch.setenv("DB_PATH", "/./test.db")
    monkeypatch.setenv("SECRET_KEY", "notsosecretive")
    monkeypatch.setenv("SECRET_KEY_N_BYTES", "42")
    monkeypatch.setenv("ALGORITHM", "secure")

    got = get_settings()
    want = Settings(
        log_level="critical",
        db_path="/./test.db",
        secret_key="notsosecretive",
        secret_key_n_bytes=42,
        algorithm="secure",
    )
    assert got == want


@pytest.mark.parametrize(
    "level, want",
    [
        ("critical", logging.CRITICAL),
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
        ("trace", TRACE_LOG_LEVEL),
    ],
)
def test_get_log_level(level: LogLevel, want: int):
    got = get_log_level(level)
    assert got == want


@pytest.mark.parametrize("level", ["fatal", "scary", "few"])
def test_get_bad_log_level(level: LogLevel):
    exc = f"{level=} invalid. Log levels: critical, error, warning, info, debug, trace"
    with pytest.raises(RuntimeError, match=exc):
        get_log_level(level)
