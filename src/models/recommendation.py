from dataclasses import dataclass


@dataclass
class Recommendation:

    symbol: str

    price: float

    ai_score: float

    rating: str

    sector: str

    rsi: float

    ma50: float

    ma200: float

    bullish_trend: bool

    portfolio_fit_score: float