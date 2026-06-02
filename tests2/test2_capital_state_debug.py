from src.services.capital_service import (
    CapitalService
)

state = (
    CapitalService
    .build_capital_state()
)

print()
print(state)