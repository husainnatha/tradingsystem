from app.engine.portfolio_summary import (
    get_portfolio_summary
)

summary = (
    get_portfolio_summary()
)

print("\nPORTFOLIO SUMMARY:\n")

for key, value in summary.items():

    print(
        f"{key}: {value}"
    )