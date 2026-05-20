from pathlib import Path
from datetime import datetime

import pandas as pd

# -----------------------------------
# BASE DIRECTORY
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

tax_state_path = (

    BASE_DIR

    / "data"

    / "tax_state"

    / "tax_state.csv"
)

# -----------------------------------
# LOAD TAX STATE
# -----------------------------------


def load_tax_state():

    if not tax_state_path.exists():

        empty_df = pd.DataFrame(

            columns=[

                "tax_year",
                "carried_losses_gbp",
                "net_gain_gbp",
                "estimated_cgt_due_gbp",
                "last_updated"
            ]
        )

        empty_df.to_csv(
            tax_state_path,
            index=False
        )

    return pd.read_csv(
        tax_state_path
    )

# -----------------------------------
# SAVE TAX STATE
# -----------------------------------


def save_tax_state(

    tax_year,
    carried_losses_gbp,
    net_gain_gbp,
    estimated_cgt_due_gbp
):

    df = load_tax_state()

    # Remove existing row

    df = df[
        df["tax_year"] != tax_year
    ]

    new_row = {

        "tax_year":
            tax_year,

        "carried_losses_gbp":
            carried_losses_gbp,

        "net_gain_gbp":
            net_gain_gbp,

        "estimated_cgt_due_gbp":
            estimated_cgt_due_gbp,

        "last_updated":
            datetime.now()
    }

    df = pd.concat(

        [

            df,

            pd.DataFrame(
                [new_row]
            )
        ],

        ignore_index=True
    )

    df.to_csv(
        tax_state_path,
        index=False
    )

# -----------------------------------
# GET CARRIED LOSSES
# -----------------------------------


def get_carried_losses(
    tax_year
):

    df = load_tax_state()

    row = df[
        df["tax_year"] == tax_year
    ]

    if row.empty:

        return 0

    return float(

        row.iloc[0][
            "carried_losses_gbp"
        ]
    )

# -----------------------------------
# GET PREVIOUS TAX YEAR
# -----------------------------------

def get_previous_tax_year(
    tax_year
):

    start_year = int(
        tax_year.split("/")[0]
    )

    previous_start = (
        start_year - 1
    )

    previous_end = start_year

    return (
        f"{previous_start}/"
        f"{previous_end}"
    )

# -----------------------------------
# AUTO CARRY FORWARD LOSSES
# -----------------------------------


def get_auto_carried_losses(
    tax_year
):

    previous_tax_year = (
        get_previous_tax_year(
            tax_year
        )
    )

    df = load_tax_state()

    row = df[
        df["tax_year"]
        ==
        previous_tax_year
    ]

    if row.empty:

        return 0

    return float(

        row.iloc[0][
            "carried_losses_gbp"
        ]
    )