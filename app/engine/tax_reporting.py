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

    ledger = (

        build_disposal_ledger()
    )

    if ledger.empty:

        return {}

    filtered = (

        ledger[
            ledger["tax_year"]

            == tax_year
        ]
    )

    if filtered.empty:

        return {}

    total_proceeds = (

        filtered[
            "proceeds_gbp"
        ].sum()
    )

    total_gains = (

        filtered[
            filtered[
                "gain_loss_gbp"
            ] > 0
        ][
            "gain_loss_gbp"
        ].sum()
    )

    total_losses = (

        filtered[
            filtered[
                "gain_loss_gbp"
            ] < 0
        ][
            "gain_loss_gbp"
        ].abs().sum()
    )

    net_gain = (

        filtered[
            "gain_loss_gbp"
        ].sum()
    )

    return {

        "tax_year":
            tax_year,

        "disposal_count":
            len(
                filtered
            ),

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