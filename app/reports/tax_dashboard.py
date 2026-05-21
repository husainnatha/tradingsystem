from app.engine.disposal_ledger import (
    build_disposal_ledger
)

from app.config.tax_config import (
    get_tax_config
)


def build_tax_dashboard():

    df = build_disposal_ledger()

    summary_rows = []

    grouped = df.groupby("tax_year")

    for tax_year, group in grouped:

        config = get_tax_config(
            tax_year
        )

        total_gains = (

            group[
                group[
                    "gain_loss_gbp"
                ] > 0
            ][
                "gain_loss_gbp"
            ].sum()
        )

        total_losses = (

            group[
                group[
                    "gain_loss_gbp"
                ] < 0
            ][
                "gain_loss_gbp"
            ].sum()
        )

        net_gain = group[
            "gain_loss_gbp"
        ].sum()

        cgt_allowance = config[
            "cgt_allowance"
        ]

        taxable_gain = max(

            0,

            net_gain - cgt_allowance
        )

        estimated_cgt = (

            taxable_gain *

            config[
                "higher_cgt_rate"
            ]
        )

        summary_rows.append({

            "tax_year":
                tax_year,

            "total_gains":
                round(total_gains, 2),

            "total_losses":
                round(total_losses, 2),

            "net_gain":
                round(net_gain, 2),

            "cgt_allowance":
                cgt_allowance,

            "taxable_gain":
                round(taxable_gain, 2),

            "estimated_cgt":
                round(estimated_cgt, 2)
        })

    return summary_rows