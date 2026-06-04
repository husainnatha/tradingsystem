from datetime import (
    datetime,
    UTC
)

from app.engine.capital_engine import (
    build_capital_state
)

from src.services.capital_service import (
    CapitalService
)


class PortfolioHistoryService:

    @staticmethod
    def build_snapshot():

        capital_state = (
            build_capital_state()
        )

        return {

            "snapshot_date":
                datetime.now(
                    UTC
                ).strftime(
                    "%Y-%m-%d"
                ),

            "portfolio_value":
                capital_state[
                    "portfolio_value"
                ],

            "invested_value":
                capital_state[
                    "invested_value"
                ],

            "cash":
                capital_state[
                    "cash"
                ],

            "cash_contributions":
                CapitalService()
                .get_capital_config()[
                    "cash_contributions"
                ],

            "capital_status":
                capital_state[
                    "capital_status"
                ],

            "cash_funding_ratio":
                capital_state[
                    "cash_funding_ratio"
                ]
        }