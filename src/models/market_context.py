class MarketContext:

    def __init__(self):

        self.market_data = {}

    def add_dataset(
        self,
        ticker: str,
        df
    ):

        self.market_data[ticker] = df

    def get_dataset(
        self,
        ticker: str
    ):

        return self.market_data.get(ticker)

    def get_all(self):

        return self.market_data
    
    def get_tickers(self):

        return list(
            self.market_data.keys()
        )