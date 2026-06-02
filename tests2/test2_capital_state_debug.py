from app.engine.capital_engine import (
    build_capital_state
)

state = (
    build_capital_state()
)

print()

for key, value in state.items():

    print(
        f"{key}: {value}"
    )