from app.engine.macro_regime_engine import (
    build_macro_regime
)

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