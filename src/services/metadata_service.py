class MetadataService:
    def __init__(self, metadata: dict):
        self.metadata = metadata

    def get(self, ticker: str):
        return self.metadata.get(ticker)
    