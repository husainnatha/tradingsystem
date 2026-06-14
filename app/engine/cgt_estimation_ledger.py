import pandas as pd

from src.config.environment_loader import (
    EnvironmentLoader
)

from app.engine.cgt_estimator import (
    estimate_cgt
)

from app.engine.disposal_ledger import (
    build_disposal_ledger
)


def build_cgt_estimation_ledger():

    config = (
        EnvironmentLoader.load()
    )

    tax_config = (

        config[
            "uk_tax_config"
        ]
    )

    cgt_ledger_df = []

    ledger = (

        build_disposal_ledger()
    )

    for tax_year, tax_year_config in (

        tax_config.items()
    ):

        cgt_ledger_df.append(

            estimate_cgt(

                tax_year=tax_year,

                taxable_income=

                    tax_year_config[
                        "taxable_income"
                    ],

                ledger=ledger
            )
        )

    return (

        pd.DataFrame(cgt_ledger_df)

        .sort_values(
            by="tax_year"
        )

        .reset_index(
            drop=True
        )
    )