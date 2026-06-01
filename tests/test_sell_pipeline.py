from src.pipelines.sell_pipeline import (
    SellPipeline
)

pipeline = (
    SellPipeline()
)

pipeline.run_sell_analysis()

print(
            "\nPipeline complete.\n"
        )