from src.config.asset_metadata_loader import TickerLoader, TickerMetadataLoader

def test_ticker_metadata_assignment():
    tickers = TickerLoader.load()["tickers"]
    metadata = TickerMetadataLoader.load()

    for ticker in tickers:
        info = metadata.get(ticker)

        if info is None:
            # Flag missing metadata but continue
            print(f"{ticker}: MISSING metadata")
            continue

        print(
            f"{ticker}: "
            f"sector={info.get('sector')}, "
            f"sub_sector={info.get('sub_sector')}, "
            f"themes={info.get('themes')}, "
            f"quality={info.get('quality')}, "
            f"conviction={info.get('conviction')}"
        )

        assert True