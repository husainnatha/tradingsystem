from app.engine.cgt_estimator import (
    estimate_cgt
)

# -----------------------------------
# TEST PARAMETERS
# -----------------------------------

tax_year = "2025/26"

taxable_income = 60000

# -----------------------------------
# RUN ESTIMATE
# -----------------------------------

results = estimate_cgt(

    tax_year=tax_year,

    taxable_income=taxable_income
)

# -----------------------------------
# OUTPUT
# -----------------------------------

print("\nCGT ESTIMATE:\n")

for key, value in results.items():

    print(
        f"{key}: {value}"
    )