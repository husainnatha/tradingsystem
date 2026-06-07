from app.engine.matching_engine import (
    get_section_104_pool
)


results = get_section_104_pool()

print("\nSECTION 104 DISPOSALS:\n")

for disposal in results[
    "section_104_disposals"
]:

    print(

        f"{disposal}"
    )