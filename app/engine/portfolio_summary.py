from app.engine.portfolio_valuation import (
    get_portfolio_valuation
)


def get_portfolio_summary():

    portfolio = (
        get_portfolio_valuation()
    )

    if not portfolio:

        return {

            "total_portfolio_value":
                0,

            "total_unrealised_pl":
                0,

            "total_holdings":
                0
        }

    total_value = sum(

        row[
            "market_value"
        ]

        for row in portfolio
    )

    total_unrealised_pl = sum(

        row[
            "unrealised_pl"
        ]

        for row in portfolio
    )

    total_holdings = len(
        portfolio
    )

    largest_position = max(

        portfolio,

        key=lambda x:
            x["market_value"]
    )

    best_performer = max(

        portfolio,

        key=lambda x:
            x["unrealised_pl"]
    )

    worst_performer = min(

        portfolio,

        key=lambda x:
            x["unrealised_pl"]
    )

    return {

        "total_portfolio_value":
            round(
                total_value,
                2
            ),

        "total_unrealised_pl":
            round(
                total_unrealised_pl,
                2
            ),

        "total_holdings":
            total_holdings,

        "largest_position":
            largest_position[
                "symbol"
            ],

        "largest_position_value":
            round(
                largest_position[
                    "market_value"
                ],
                2
            ),

        "best_performer":
            best_performer[
                "symbol"
            ],

        "best_performer_pl":
            round(
                best_performer[
                    "unrealised_pl"
                ],
                2
            ),

        "worst_performer":
            worst_performer[
                "symbol"
            ],

        "worst_performer_pl":
            round(
                worst_performer[
                    "unrealised_pl"
                ],
                2
            )
    }