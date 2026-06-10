from src.pipelines.system_pipeline import (
    SystemPipeline
)


def run_pipeline():

    pipeline = SystemPipeline()

    pipeline.run()


if __name__ == "__main__":

    run_pipeline()