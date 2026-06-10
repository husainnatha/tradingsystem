from src.config.environment_loader import (
    EnvironmentLoader
)


def test_print_config():

    config = (
        EnvironmentLoader
        .load()
    )

    print()
    print(config)
    print()

    assert config is not None