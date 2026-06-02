from app.engine.capital_engine import (
    build_capital_state,
    build_capital_summary
)


class CapitalPipeline:

    def run(self):

        return {

            "capital_state":
                build_capital_state(),

            "capital_summary":
                build_capital_summary()
        }