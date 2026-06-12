from app.engine.macro_regime_engine import (
    build_macro_regime
)

def test_macro_regime_engine ():

    regime = build_macro_regime()

    print(
        "\nMACRO REGIME\n"
    )

    print(

        f"Regime: "

        f"{regime['regime']}"
    )

    print(

        f"Score: "

        f"{regime['score']}"
    )

    print(
        "\nDrivers:\n"
    )

    for reason in regime[
        "reasons"
    ]:

        print(

            f"- {reason}"
        )
    
    assert len(regime) > 0

assert True