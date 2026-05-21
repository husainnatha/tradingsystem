import pandas as pd

from app.engine.holdings_service import (
    calculate_holdings
)

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

    summary_df = pd.DataFrame(
        summary_rows
    )

    return summary_df

# -----------------------------------
# EXPORT TAX DASHBOARD
# -----------------------------------

def export_tax_dashboard_to_excel():

    # -----------------------------------
    # BUILD DATAFRAMES
    # -----------------------------------

    summary_df = build_tax_dashboard()

    disposal_df = build_disposal_ledger()

    # -----------------------------------
    # HOLDINGS DATAFRAME
    # -----------------------------------

    holdings = calculate_holdings()

    holdings_rows = []

    for symbol, data in holdings.items():

        holdings_rows.append({

            "symbol":
                symbol,

            "quantity":
                round(
                    data["quantity"],
                    2
                ),

            "pool_cost_gbp":
                round(
                    data["pool_cost"],
                    2
                ),

            "average_cost_gbp":
                round(
                    data["avg_cost"],
                    2
                ),

            "realised_pnl_gbp":
                round(
                    data["realised_pnl"],
                    2
                )
        })

    holdings_df = pd.DataFrame(
        holdings_rows
    )

    # -----------------------------------
    # EXPORT TO EXCEL
    # -----------------------------------

    output_path = (

        "dashboard/"
        "tax_dashboard.xlsx"
    )

    with pd.ExcelWriter(

        output_path,

        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(

            writer,

            sheet_name="TAX_SUMMARY",

            index=False
        )

        disposal_df.to_excel(

            writer,

            sheet_name="DISPOSAL_LEDGER",

            index=False
        )

        holdings_df.to_excel(

            writer,

            sheet_name="HOLDINGS",

            index=False
        )

    print(

        f"\nTax dashboard exported:\n"
        f"{output_path}\n"
    )