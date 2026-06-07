from src.pipelines.export_intelligence_report_pipeline import (
    ExportIntelligenceReportPipeline
)

def test_export_intelligence_report_pipeline():

    ExportIntelligenceReportPipeline.run_pipeline()

    assert True