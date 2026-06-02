from src.services.spreadsheet_capital_loader import (
    SpreadsheetCapitalLoader
)


def test_spreadsheet_capital_loader():

    config = (
        SpreadsheetCapitalLoader
        .load()
    )

    assert (
        isinstance(
            config,
            dict
        )
    )

    assert (
        config["cash"]
        >= 0
    )

    assert (
        config[
            "target_cash_reserve"
        ]
        > 0
    )

    assert (
        config[
            "emergency_reserve"
        ]
        > 0
    )

    assert (
        config[
            "cash_contributions"
        ]
        >= 0
    )

    assert (
        config[
            "max_deployment_percent"
        ]
        > 0
    )