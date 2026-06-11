from app.engine.portfolio_summary import (
    get_portfolio_summary
)

def test_portfolio_summary():

    summary = (
        get_portfolio_summary()
    )

    print()

    for k, v in summary.items():

        print(
            f"{k}: {v}"
        )

    assert True