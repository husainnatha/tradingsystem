from src.services.portfolio_history_service import (
    PortfolioHistoryService
)

def test_portfolio_snapshot():

    snapshot = (
        PortfolioHistoryService
        .build_snapshot()
    )

    print()

    print(snapshot)

    print()

    for k, v in snapshot.items():

        print(
            f"{k}: {v}"
        )

    assert isinstance(
        snapshot,
        dict
    )

    assert (
        snapshot[
            "portfolio_value"
        ] >= 0
    )