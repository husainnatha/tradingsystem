from app.engine.tax_reporting import (
    generate_tax_year_summary
)

summary = generate_tax_year_summary(
    "2025/2026"
)

print("\nUK TAX YEAR SUMMARY:\n")

for key, value in summary.items():

    print(
        f"{key}: {value}"
    )