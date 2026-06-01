from src.data.loaders.market_data_loader import MarketDataLoader

loader = MarketDataLoader()

df = loader.load(
    ticker="GC=F",
    period="2y"
)

print(df.tail())