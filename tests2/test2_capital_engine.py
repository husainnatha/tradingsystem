from app.engine.capital_engine import (
    build_capital_summary
)


def test_capital_engine():

    df = (
        build_capital_summary()
    )

    print(
        "\nCAPITAL SUMMARY:\n"
    )   
    print(df)

    assert True