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

        cash_percentage = round(

    (
        cash
        /
        portfolio_value
    ) * 100,

    2

        ) if portfolio_value != 0 else 0


        invested_percentage = round(

            (
                invested_value
                /
                portfolio_value
            ) * 100,

            2

        ) if portfolio_value != 0 else 0


        cash_funding_ratio = round(

            cash
            /
            target_cash_reserve,

            2

        ) if target_cash_reserve != 0 else 0

        max_deployment_percent = (
            config[
                "max_deployment_percent"
            ]
        )

        target_invested_value = round(

            portfolio_value

            * (

                max_deployment_percent
                / 100
            ),

            2
        )

        deployment_difference = round(

            invested_value

            - target_invested_value,

            2
        )

        required_sale_value = max(

            0,

            deployment_difference
        )

        available_cash = max(

            0,

            cash

            - target_cash_reserve
        )

        deployable_capital = min(

            available_cash,

            max(
                0,
                -deployment_difference
            )
        )

        required_sale_for_cash = (
            cash_shortfall
        )

        required_sale_for_deployment = max(
            0,
            deployment_difference
        )

        cash_target_achievable = (
            required_sale_for_cash
            <=
            portfolio_value
        )

        if cash_funding_ratio < 0.5:

            capital_status = "CRITICAL"

        elif cash_funding_ratio < 1:

            capital_status = "UNDERFUNDED"

        elif deployment_difference > 0:

            capital_status = "OVERDEPLOYED"

        else:

            capital_status = "HEALTHY"

            cash_funding_ratio = round(

            portfolio_value

            /

            target_cash_reserve,

            2
        )
            
            cash_percentage,

            invested_percentage,

            cash_funding_ratio,
        
            cash_percentage = round(

            (
                cash
                /
                portfolio_value
            ) * 100,

            2

        ) if portfolio_value != 0 else 0


        invested_percentage = round(

            (
                invested_value
                /
                portfolio_value
            ) * 100,

            2

        ) if portfolio_value != 0 else 0

        return {
            "cash":
                cash,
            "target_cash_reserve":
                target_cash_reserve,
            "cash_shortfall":
                cash_shortfall,
            "cash_surplus":
                cash_surplus,
            "portfolio_value":
                portfolio_value,
            "invested_value":
                invested_value,
            "max_deployment_percent":
                max_deployment_percent,
            "target_invested_value":
                target_invested_value,
            "deployment_difference":
                deployment_difference,
            "required_sale_value":
                required_sale_value,
            "available_cash":
                available_cash,
            "deployable_capital":
                deployable_capital,
            "required_sale_for_cash":
                required_sale_for_cash,
            "required_sale_for_deployment":
                required_sale_for_deployment,
            "cash_target_achievable":
                cash_target_achievable,
            "capital_status":
                capital_status,
            "cash_funding_ratio":
                cash_funding_ratio,
            "cash_percentage":
                cash_percentage,
            "invested_percentage":
                invested_percentage,
            "cash_funding_ratio":
                cash_funding_ratio
        }
        