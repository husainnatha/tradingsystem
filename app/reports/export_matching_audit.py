from pathlib import Path

import pandas as pd

from app.engine.matching_engine import (
    get_same_day_matches,
    get_thirty_day_matches,
    get_section_104_pool
)

from app.engine.disposal_ledger import (
    build_disposal_ledger
)

from app.config.environment import (

    EXPORT_DIR,

    get_output_suffix
)

def run_matching_audit(
                

):

    # -----------------------------------
    # BASE DIRECTORY
    # -----------------------------------

    env = get_output_suffix()

    export_dir = (
    EXPORT_DIR
    / "matching_audit"
    )

    export_dir.mkdir(
    parents=True,
    exist_ok=True
    )

    output_file = (

    EXPORT_DIR 
    / "matching_audit"
    / f"{env}-matching-audit.xlsx"
    )


    print(
    f"\nExport directory:\n{export_dir}\n"
    )

    # -----------------------------------
    # SAME-DAY MATCHES
    # -----------------------------------

    same_day_results = (
    get_same_day_matches()
    )

    same_day_df = pd.DataFrame(
    same_day_results[
        "matches"
    ]
    )

    with pd.ExcelWriter(

        output_file,

        engine="xlsxwriter"

    ) as writer:

        same_day_df.to_excel(

            writer,

            sheet_name="SAME_DAY",

            index=False
        )

    print(
    f"Exported SAME DAY"
    )

    # -----------------------------------
    # THIRTY-DAY MATCHES
    # -----------------------------------

    thirty_day_results = (
    get_thirty_day_matches()
    )

    thirty_day_df = pd.DataFrame(
    thirty_day_results[
        "thirty_day_matches"
    ]
    )

    with pd.ExcelWriter(

        output_file,

        engine="xlsxwriter"

    ) as writer:

        thirty_day_df.to_excel(

            writer,

            sheet_name="THIRTY_DAY",

            index=False
        )

    print(
    f"Exported THIRTY DAY"
    )
    # -----------------------------------
    # SECTION 104 DISPOSALS
    # -----------------------------------

    s104_results = (
    get_section_104_pool()
    )

    s104_df = pd.DataFrame(
    s104_results[
        "section_104_disposals"
    ]
    )

    with pd.ExcelWriter(

        output_file,

        engine="xlsxwriter"

    ) as writer:

        s104_df.to_excel(

            writer,

            sheet_name="SECTION_104_DISPOSALS",

            index=False
        )

    print(
    f"Exported SECTION 104 DISPOSALS"
    )

    # -----------------------------------
    # DISPOSAL LEDGER
    # -----------------------------------

    ledger = build_disposal_ledger()

    ledger_df = pd.DataFrame(
    ledger
    )

    with pd.ExcelWriter(

        output_file,

        engine="xlsxwriter"

    ) as writer:

        ledger_df.to_excel(

            writer,

            sheet_name="DISPOSALS_LEDGER",

            index=False
        )

    print(
    f"Exported DISPOSALS LEDGER"
    )
    print(
    "\nMatching audit export complete.\n"
    )
