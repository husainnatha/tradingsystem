from app.engine.sector_intelligence import (
    build_sector_exposure
)

def test_sector_intelligence_engine():

    df = build_sector_exposure()

    print("\nSECTOR EXPOSURE:\n")

    for _, row in df.iterrows():

        print(

            f"{row['sector']} | "

            f"Exposure={row['exposure_pct']}% | "

            f"Risk={row['concentration_risk']}"
        )

    assert True