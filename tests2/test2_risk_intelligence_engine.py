from app.engine.risk_intelligence_engine import (
    build_risk_engine
)


def test_risk_intelligence_engine():

    risk_intelligence_df = (

        build_risk_engine(

            verbose=True
        )

        .sort_values(


            by="asset_risk_score",

            ascending=False
        )
    )

    print(

        "\nRISK INTELLIGENCE:\n"
    )

    print(

        print(risk_intelligence_df)
    )

    assert len(risk_intelligence_df) > 1
    assert True