import pytest

from app.config import Environment, Settings
from app.core.cors import allowed_origins


def test_local_origins_are_added_outside_production():
    settings = Settings(environment=Environment.LOCAL, cors_allowed_origins="")
    assert "http://localhost:8081" in allowed_origins(settings)


def test_production_does_not_get_localhost_for_free():
    settings = Settings(
        environment=Environment.PRODUCTION,
        cors_allowed_origins="https://tablr.app",
    )
    assert allowed_origins(settings) == ["https://tablr.app"]


def test_wildcard_origin_is_rejected():
    settings = Settings(
        environment=Environment.PRODUCTION, cors_allowed_origins="*"
    )
    with pytest.raises(ValueError):
        allowed_origins(settings)
