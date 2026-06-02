from src.services.capital_service import (
    CapitalService
)


def test_capital_state():

    state = (
        CapitalService
        .build_capital_state()
    )

    assert (
        "target_invested_value"
        in state
    )

    assert (
        "deployment_difference"
        in state
    )

    assert (
        state[
            "target_invested_value"
        ] >= 0
    )