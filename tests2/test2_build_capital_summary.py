from app.engine.capital_engine import (
    build_capital_summary
)

def test_build_capital_summary(
        
):
    
    df = build_capital_summary()

    print(df)

    assert len(df) >= 1
    assert True