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