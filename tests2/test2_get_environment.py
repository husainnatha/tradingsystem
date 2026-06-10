from src.config.environment_loader import (
    EnvironmentLoader
)


def test_get_environment():

    environment = (
        EnvironmentLoader
        .get_environment()
    )

    assert environment in [
        "dev",
        "prod",
        "test"
    ]