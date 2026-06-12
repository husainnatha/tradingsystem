from app.engine.buy_recommendation_engine import (
    build_buy_recommendations
)


from src.pipelines.market_pipeline import (
    MarketPipeline
)

def test_buy_reccomendations_engine():

    pipeline = MarketPipeline()

    market_context = pipeline.run_watchlist(
        "equities"
    )
        
    df = build_buy_recommendations(

        market_context=market_context,
    )

    print("\nBUY RECOMMENDATIONS:\n")

    for _, row in df.iterrows():

        print(

            f"{row['symbol']} | "

            f"AI={row['ai_score']} | "

            f"Rating={row['rating']} | "

            f"RSI={row['rsi']} | "

            f"Fit={row['portfolio_fit_score']} \n"

            f"Why: {row['explanation']}\n"
        )
    
    assert True