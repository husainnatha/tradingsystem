import pandas as pd

from src.config.environment_loader import (
    EnvironmentLoader
)

from app.engine.cgt_estimator import (
    estimate_cgt
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

    rows = []

    for tax_year, tax_year_config in (

        tax_config.items()
    ):

        rows.append(

            estimate_cgt(

                tax_year=tax_year,

                taxable_income=

                    tax_year_config[
                        "taxable_income"
                    ]
            )
        )

    return (

        pd.DataFrame(rows)

        .sort_values(
            by="tax_year"
        )

        .reset_index(
            drop=True
        )
    )