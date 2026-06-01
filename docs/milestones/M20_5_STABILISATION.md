[/] test_pipeline
[/] test_system_pipeline
[/] test_market_pipeline

[/] test_market_intelligence
[/] test_position_sizing
[/] test_rebalancing
[/] test_portfolio_risk

[/] test_action_engine
[/] test_decision_engine
[/] test_transition_engine

[/] test_tax_dashboard
[/] test_disposal_ledger


CATEGORY1 - MACRO REQUIRED
/ macro_regime_engine
/ position_sizing_engine
/ rebalancing_engine
/ action_engine
/ transition_engine

CATEGORY2 - MACRO OPTIONAL
/ market_intelligence_engine
/ buy_recommendation_engine
/ recommendation_mapper
/ sector_intelligence
/ correlation_engine
/ portfolio_risk_engine

CATEGORY3 - MACRO NOT REQUIRED
/ inventory_engine
/ holdings_service
/ disposal_ledger
/ tax_dashboard
/ matching_ledger
/ section_104
/ capital_engine
/ portfolio_valuation

python -m tests.test_position_sizing
python -m tests.test_rebalancing
python -m tests.test_action_engine
python -m tests.test_transition_engine

Refactoring
Rename risk_score → asset_risk_score
Remove dead parameters
Remove duplicated code
Standardise engine signatures

Performance
Avoid rebuilding portfolio risk repeatedly
Avoid rebuilding tax dashboard repeatedly
Introduce engine caching

Features
Macro regime integration
Portfolio optimisation
Tax-aware selling
Sector allocation control

risk_score_mappings

asset_risk_score
    volatility + drawdown

portfolio_risk
    concentration + correlation

position_risk_score
    inventory ranking risk