from src.services.capital_service import (
    CapitalService
)


def test_capital_state():

    state = (

        CapitalService()
        .build_capital_state()
    )

    assert "cash" in state

    assert (
        "cash_shortfall"
        in state
    )

    assert (
        "cash_surplus"
        in state
    )