from app.engine.tax_state import (
    get_auto_carried_losses,
    save_tax_state
)

from app.engine.tax_reporting import (
    generate_tax_year_summary
)

from src.config.environment_loader import (
    EnvironmentLoader
)

# -----------------------------------
# CGT ESTIMATION ENGINE
# -----------------------------------


def estimate_cgt(
    tax_year,
    taxable_income,
    ledger
):
 
    config = (
        EnvironmentLoader
        .load()
    )

    tax_config = (

        config[
            "uk_tax_config"
        ][
            tax_year
        ]
    )

    taxable_income = (

        tax_config[
            "taxable_income"
        ]
    )
    
    summary = generate_tax_year_summary(

        tax_year=tax_year,

        ledger=ledger
    )

    if not summary:

        summary = {

            "net_gain_gbp": 0
        }

        return {

            "tax_year":
                tax_year,

            "taxable_income_gbp":
                round(
                    taxable_income,
                    2
                ),

            "net_gain_gbp":
                0,

            "cgt_allowance_gbp":
                tax_config["cgt_allowance"
                ],

            "taxable_gain_gbp":
                0,

            "estimated_cgt_due_gbp":
                0
        }

    net_gain = summary[
        "net_gain_gbp"
    ]

    allowance = tax_config[
        "cgt_allowance"
    ]

    carried_losses = (
        get_auto_carried_losses(
            tax_year
        )
    )

    basic_band_limit = tax_config[
        "basic_income_limit"
    ]

    basic_cgt_rate = tax_config[
        "basic_cgt_rate"
    ]

    higher_cgt_rate = tax_config[
        "higher_cgt_rate"
    ]

    # -----------------------------------
    # TAXABLE GAIN
    # -----------------------------------

    gain_after_allowance = max(

        0,

        net_gain - allowance
    )

    taxable_gain = max(

        0,

        gain_after_allowance - carried_losses
    )

    losses_used = min(

        carried_losses,

        gain_after_allowance
    )

    remaining_carried_losses = max(

        0,

        carried_losses - losses_used
    )

    remaining_allowance = max(

        0,

        allowance - net_gain
    )

    # -----------------------------------
    # REMAINING BASIC BAND
    # -----------------------------------

    remaining_basic_band = max(

        0,

        basic_band_limit - taxable_income
    )

    # -----------------------------------
    # SPLIT GAINS
    # -----------------------------------

    basic_rate_gain = min(

        taxable_gain,

        remaining_basic_band
    )

    higher_rate_gain = max(

        0,

        taxable_gain - basic_rate_gain
    )

    # -----------------------------------
    # CGT CALCULATION
    # -----------------------------------

    estimated_cgt_due = (

        basic_rate_gain *

        basic_cgt_rate

        +

        higher_rate_gain *

        higher_cgt_rate
    )

    save_tax_state(

        tax_year=tax_year,

        carried_losses_gbp=
            remaining_carried_losses,

        net_gain_gbp=
            net_gain,

        estimated_cgt_due_gbp=
            estimated_cgt_due
    )

    return {

        "tax_year":
            tax_year,

        "taxable_income_gbp":
            round(
                taxable_income,
                2
            ),

        "net_gain_gbp":
            round(
                net_gain,
                2
            ),

        "cgt_allowance_gbp":
            round(
                allowance,
                2
            ),
        "remaining_cgt_allowance_gbp":
            round(
                remaining_allowance,
                2
            ),
        "carried_losses_gbp":
            round(
                carried_losses,
                2
            ),

        "losses_used_gbp":
            round(
                losses_used,
                2
            ),

        "remaining_carried_losses_gbp":
            round(
                remaining_carried_losses,
                2
            ),
        "taxable_gain_gbp":
            round(
                taxable_gain,
                2
            ),

        "remaining_basic_band_gbp":
            round(
                remaining_basic_band,
                2
            ),

        "basic_rate_gain_gbp":
            round(
                basic_rate_gain,
                2
            ),

        "higher_rate_gain_gbp":
            round(
                higher_rate_gain,
                2
            ),

        "estimated_cgt_due_gbp":
            round(
                estimated_cgt_due,
                2
            )
    }

# if __name__ == "__main__":


#     result = estimate_cgt(
#         tax_year,
#         taxable_income
#     )

#     print()

#     for key, value in result.items():

#         print(f"{key}: {value}")

#     print()