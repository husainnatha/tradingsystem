from app.engine.disposal_simulator import (
    simulate_sale
)

result = simulate_sale(

    symbol="POET",

    quantity=50,

    sell_price=20
)

print("\nDISPOSAL SIMULATION:\n")

for key, value in result.items():

    print(f"{key}: {value}")