import os

from src.config.environment_loader import (
    EnvironmentLoader
)

def test_environment_loader():

    # os.environ[
    #     "APP_ENV"
    # ] = "dev"

    # config = (
    #     EnvironmentLoader
    #     .load()
    # )

    env = EnvironmentLoader.get_environment()

    capital_config = EnvironmentLoader.load(
        f"config/capital/{env}.yaml"
    )

    tax_config = EnvironmentLoader.load(
        f"config/tax/{env}.yaml"
    )

    assert "capital" in capital_config

    assert (
        capital_config["capital"][
            "emergency_reserve"
        ]
        == 12000
    )

    assert (
        capital_config["capital"][
            "target_cash_reserve"
        ]
        == 12000
    )

    assert (

        tax_config["uk_tax_config"][
            "2023/24"
        ][
            "cgt_allowance"
        ]

        == 6000
    )

    print(tax_config)
    print(capital_config)