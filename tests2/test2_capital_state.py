from app.engine.capital_engine import (
    build_capital_state
)


def test_capital_state():

    state = (
        build_capital_state()
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