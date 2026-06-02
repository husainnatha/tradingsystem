from src.services.capital_service import (
    CapitalService
)

state = (
    CapitalService
    .build_capital_state()
)

print()

for key, value in state.items():

    print(
        f"{key}: {value}"
    )