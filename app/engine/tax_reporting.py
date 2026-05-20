from datetime import date

from app.engine.disposal_ledger import (
    build_disposal_ledger
)


def get_uk_tax_year(
    disposal_date
):

    year = disposal_date.year

    tax_year_start = date(
        year,
        4,
        6
    )

    if disposal_date >= tax_year_start:

        start_year = year
        end_year = year + 1

    else:

        start_year = year - 1
        end_year = year

    return (
        f"{start_year}/"
        f"{end_year}"
    )


def generate_tax_year_summary(
    tax_year
):

    ledger = build_disposal_ledger()

    filtered_rows = []

    for row in ledger:

        row_tax_year = (
            get_uk_tax_year(
                row[
                    "disposal_date"
                ]
            )
        )

        if row_tax_year == tax_year:

            filtered_rows.append(
                row
            )

    total_proceeds = sum(

        row[
            "proceeds_gbp"
        ]

        for row in filtered_rows
    )

    total_gains = sum(

        row[
            "gain_loss_gbp"
        ]

        for row in filtered_rows

        if row[
            "gain_loss_gbp"
        ] > 0
    )

    total_losses = sum(

        row[
            "gain_loss_gbp"
        ]

        for row in filtered_rows

        if row[
            "gain_loss_gbp"
        ] < 0
    )

    net_gain = sum(

        row[
            "gain_loss_gbp"
        ]

        for row in filtered_rows
    )

    return {

        "tax_year":
            tax_year,

        "disposal_count":
            len(filtered_rows),

        "total_proceeds_gbp":
            round(
                total_proceeds,
                2
            ),

        "total_gains_gbp":
            round(
                total_gains,
                2
            ),

        "total_losses_gbp":
            round(
                total_losses,
                2
            ),

        "net_gain_gbp":
            round(
                net_gain,
                2
            )
    }