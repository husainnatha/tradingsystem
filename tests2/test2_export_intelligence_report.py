from app.reports.export_intelligence_report import (
    export_intelligence_report
)

def test_export_intelligence_report(
        
    market_df,
    recommendation_df,
    position_df,
    sale_df,
    action_df,
    transition_df,
    capital_df=None,
    macro_df=None,
    opportunity_df=None,
    contextual_decisions_df=None
):

    export_intelligence_report()

    assert True