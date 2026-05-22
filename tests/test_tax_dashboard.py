from app.reports.tax_dashboard import (
    build_tax_dashboard
)

dashboard = build_tax_dashboard()

print("\nTAX DASHBOARD:\n")

for _, row in dashboard.iterrows():

    print(

        f"{row['tax_year']} | "

        f"Gains=£{row['total_gains']} | "

        f"Losses=£{row['total_losses']} | "

        f"Net=£{row['net_gain']} | "

        f"Allowance=£{row['cgt_allowance']} | "

        f"Taxable=£{row['taxable_gain']} | "

        f"Estimated CGT=£{row['estimated_cgt']}"
    )