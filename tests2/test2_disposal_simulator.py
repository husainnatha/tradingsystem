from app.engine.disposal_simulator import (
    simulate_sale
)

def test_disposal_simulator_engine():

    result = simulate_sale(

        symbol="POET",

        quantity=50,

        sell_price=20
    )

    print("\nDISPOSAL SIMULATION:\n")

    for key, value in result.items():

        print(f"{key}: {value}")

    assert True
    assert(result) is not None