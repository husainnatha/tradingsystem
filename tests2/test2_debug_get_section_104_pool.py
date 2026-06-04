from app.engine.matching_engine import (
    get_section_104_pool
)

def test_section_104_pool():

    results = (
        get_section_104_pool()
    )

    pool = (
        results[
            "remaining_pool"
        ]
    )

    print()

    print(
        f"Positions: {len(pool)}"
    )

    print()

    for symbol, data in pool.items():

        print(
            symbol,
            data
        )

    assert True