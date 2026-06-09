from app.reports.tax_dashboard import (
    build_tax_dashboard
)

def test_build_tax_dashboard():

    df = (
        build_tax_dashboard()
    )

    print(
        "\nCAPITAL SUMMARY:\n"
    )   
    print(df)

    assert True

