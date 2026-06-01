import os

from src.config.environment_loader import (
    EnvironmentLoader
)

def test_default_environment_is_prod():

    os.environ.pop(
        "APP_ENV",
        None
    )

    config = (
        EnvironmentLoader.load()
    )

    assert config is not None