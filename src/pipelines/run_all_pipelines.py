from src.pipelines.system_pipeline import (
    SystemPipeline
)

from src.pipelines.capital_pipeline import (
    CapitalPipeline
)

from src.pipelines.market_pipeline import (
    MarketPipeline
)


from src.pipelines.opportunity_pipeline import (
    OpportunityPipeline
)

from src.pipelines.position_sizing_pipeline import (
    PositionSizingPipeline
)

from src.pipelines.price_cache_pipeline import (
    PriceCachePipeline
)

from src.pipelines.sell_pipeline import (
    SellPipeline
)

from src.pipelines.export_intelligence_report_pipeline import (
    ExportIntelligenceReportPipeline
)


def run_all_pipelines():

    SystemPipeline().run()
    CapitalPipeline().run()
    MarketPipeline().run_watchlist("equities")
    OpportunityPipeline().run()
    PositionSizingPipeline().run()
    PriceCachePipeline().run()
    SellPipeline.run_sell_analysis("self")
    ExportIntelligenceReportPipeline.run_pipeline()

if __name__ == "__main__":

    run_all_pipelines()