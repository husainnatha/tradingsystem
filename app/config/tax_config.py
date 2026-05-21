# -----------------------------------
# UK TAX CONFIGURATION
# -----------------------------------

UK_TAX_CONFIG = {

    "2023/24": {

        "cgt_allowance": 6000,

        "basic_income_limit": 50270,

        "basic_cgt_rate": 0.10,

        "higher_cgt_rate": 0.20
    },

    "2024/25": {

        "cgt_allowance": 3000,

        "basic_income_limit": 50270,

        "basic_cgt_rate": 0.10,

        "higher_cgt_rate": 0.20
    },

    "2025/26": {

        "cgt_allowance": 3000,

        "basic_income_limit": 50270,

        "basic_cgt_rate": 0.10,

        "higher_cgt_rate": 0.20
    }
}

# -----------------------------------
# TAX YEAR HELPER
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
# TAX CONFIG LOOKUP
# -----------------------------------

def get_tax_config(tax_year):

    if tax_year not in UK_TAX_CONFIG:

        raise Exception(

            f"No tax config found "
            f"for {tax_year}"
        )

    return UK_TAX_CONFIG[tax_year]