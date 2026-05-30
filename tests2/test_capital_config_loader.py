from src.config.capital_config_loader import (
    CapitalConfigLoader
)


def test_capital_config_loader():

    config = (
        CapitalConfigLoader
        .load()
    )

    assert (
        config[
            "max_deployment_percent"
        ]
        == 70
    )