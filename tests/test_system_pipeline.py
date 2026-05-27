from src.pipelines.system_pipeline import (
    SystemPipeline
)


def test_system_pipeline_runs():

    pipeline = SystemPipeline()

    pipeline.ensure_directories()

    assert True