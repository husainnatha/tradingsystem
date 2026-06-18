from src.config.environment_loader import (
    EnvironmentLoader
)

def test_environment_loader():

    config = EnvironmentLoader.load(
    
    )


    assert "capital" in config

    assert (
        config["capital"][
            "emergency_reserve"
        ]
        >= 0
    )

    assert (
        config["capital"][
            "target_cash_reserve"
        ]
        >= 0
    )

    assert (

        config["uk_tax_config"][
            "2025/26"
        ][
            "cgt_allowance"
        ]

        >= 0
    )

    print(config)