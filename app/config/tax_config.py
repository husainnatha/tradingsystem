from datetime import date
from src.config.environment_loader import (
    EnvironmentLoader
)


# -----------------------------------
# TAX YEAR HELPER FOR TRADE DATE
# -----------------------------------

def get_tax_year(trade_date):

    if trade_date.month >= 4:

        return (

            f"{trade_date.year}/"
            f"{str(trade_date.year + 1)[2:]}"
        )

    return (

        f"{trade_date.year - 1}/"
        f"{str(trade_date.year)[2:]}"
    )

# -----------------------------------
# CURRENT UK CALENDAR TAX YEAR  
# -----------------------------------

def get_current_tax_year():

    return get_tax_year(
        date.today()
    )

# -----------------------------------
# TAX CONFIG LOOKUP
# -----------------------------------

def get_tax_config(tax_year):

    config = (
        EnvironmentLoader
        .load()
    )

    tax_config = (
        config[
            "uk_tax_config"
        ]
    )

    if tax_year not in tax_config:

        raise Exception(

            f"No tax config found "
            f"for {tax_year}"
        )

    return tax_config[
        tax_year
    ]