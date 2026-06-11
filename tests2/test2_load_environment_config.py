from src.config.environment_loader import (
    EnvironmentLoader
)


def test_load_environment_config():

    config = (
        EnvironmentLoader
        .load()
    )

    print()
    print(config)
    print()

    assert config is not None