import traceback
import sys

try:
    from src.pipelines.sell_pipeline import SellPipeline
except ImportError as e:
    print(f"Import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

def test_sell_pipeline():
    pipeline = SellPipeline()
    results = pipeline.run_sell_analysis()
    assert results.inventory_df is not None
    assert results.ranked_df is not None
    assert results.sell_df is not None
    print(results.inventory_df.head())
    print(results.ranked_df.head())
    print(results.sell_df.head())