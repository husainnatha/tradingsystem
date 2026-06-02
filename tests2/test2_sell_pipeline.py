import traceback
import sys

try:
    from src.pipelines.sell_pipeline import SellPipeline
except ImportError as e:
    print(f"Import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

def test_sell_pipeline():

    results = (
        SellPipeline()
        .run_sell_analysis()
    )

    assert not results.inventory_df.empty

    assert not results.ranked_df.empty

    assert results.sell_df is not None