from src.pipelines.system_pipeline import (
    SystemPipeline
)

def test_system_pipeline():

    pipeline = SystemPipeline()

    pipeline.run()

    assert True