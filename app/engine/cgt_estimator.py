from app.engine.tax_state import (
    get_auto_carried_losses,
    save_tax_state
)

from app.engine.tax_reporting import (
    generate_tax_year_summary
)

# -----------------------------------
# UK TAX CONFIGURATION
# -----------------------------------

UK_TAX_CONFIG = {

    "2025/26": {

        "CGT_ALLOWANCE":
            3000,

        "BASIC_INCOME_RATE_ALLOWANCE":
            0,

        "BASIC_CGT_RATE":
            0.10,

        "HIGHER_CGT_RATE":
            0.20
    },

    "2024/25": {

        "CGT_ALLOWANCE":
            3000,

        "BASIC_INCOME_RATE_ALLOWANCE":
            37700,

        "BASIC_CGT_RATE":
            0.10,

        "HIGHER_CGT_RATE":
            0.20
    }
}

# -----------------------------------
# CGT ESTIMATION ENGINE
# -----------------------------------


def estimate_cgt(
    tax_year,
    taxable_income=0
):

    summary = generate_tax_year_summary(
        tax_year
    )

    if tax_year not in UK_TAX_CONFIG:

        raise ValueError(
            f"Unsupported tax year: {tax_year}"
        )

    if not summary:

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
                UK_TAX_CONFIG[
                    tax_year
                ][
                    "CGT_ALLOWANCE"
                ],

            "taxable_gain_gbp":
                0,

            "estimated_cgt_due_gbp":
                0
        }

    net_gain = summary[
        "net_gain_gbp"
    ]

    tax_config = UK_TAX_CONFIG[
        tax_year
    ]

    allowance = tax_config[
        "CGT_ALLOWANCE"
    ]

    carried_losses = (
        get_auto_carried_losses(
            tax_year
        )
    )

    basic_band_limit = tax_config[
        "BASIC_INCOME_RATE_ALLOWANCE"
    ]

    basic_cgt_rate = tax_config[
        "BASIC_CGT_RATE"
    ]

    higher_cgt_rate = tax_config[
        "HIGHER_CGT_RATE"
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

if __name__ == "__main__":

    result = estimate_cgt(
        tax_year="2025/26",
        taxable_income=0
    )

    print()

    for key, value in result.items():

        print(f"{key}: {value}")

    print()