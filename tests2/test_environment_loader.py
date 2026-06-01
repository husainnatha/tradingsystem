import os

from src.config.environment_loader import (
    EnvironmentLoader
)

def test_environment_loader():

    os.environ[
        "APP_ENV"
    ] = "dev"

    config = (
        EnvironmentLoader
        .load()
    )

    assert "capital" in config

    assert (
        config["capital"][
            "emergency_reserve"
        ]
        == 12000
    )

    assert (
        config["capital"][
            "target_cash_reserve"
        ]
        == 12000
    )