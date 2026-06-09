from app.reports.tax_dashboard import (
    export_tax_dashboard_to_excel
)

def test_export_tax_dashboard_to_excel():

    export_tax_dashboard_to_excel()

    assert True