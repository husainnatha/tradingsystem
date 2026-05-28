from app.engine.capital_engine import (
    build_capital_summary
)


def test_capital_engine():

    df = (
        build_capital_summary()
    )

    print(df)

    assert not df.empty