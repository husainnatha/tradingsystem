from logging import config

from src.config.capital_config_loader import (
    CapitalConfigLoader
)

from src.services.spreadsheet_capital_loader import (
    SpreadsheetCapitalLoader
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
    )


class CapitalService:

    @staticmethod
    def get_capital_config():

        yaml_config = (
            CapitalConfigLoader
            .load()
        )

        spreadsheet_config = (
            SpreadsheetCapitalLoader
            .load()
        )

        yaml_config.update(
            spreadsheet_config
        )

        print("CONFIG =", yaml_config)
        
        return yaml_config


    @staticmethod
    def build_capital_state():

        config = (
            CapitalService
            .get_capital_config()
        )

        cash = (
            config["cash"]
        )

        target_cash_reserve = (
            config[
                "target_cash_reserve"
            ]
        )

        cash_shortfall = max(
            0,
            target_cash_reserve
            - cash
        )

        cash_surplus = max(
            0,
            cash
            - target_cash_reserve
        )

        summary = (
            get_portfolio_summary()
        )

        portfolio_value = (
            summary[
                "total_portfolio_value"
            ]
        )

        invested_value = (

            portfolio_value

            - cash
        )

        return {

            "cash": cash,

            "target_cash_reserve":
                target_cash_reserve,

            "cash_shortfall":
                cash_shortfall,

            "cash_surplus":
                cash_surplus,

            "portfolio_value":
                portfolio_value,

            "invested_value":
                invested_value
        }
