import pandas as pd


# -----------------------------------
# BUILD TRANSITION PLAN
# -----------------------------------

def build_transition_plan(

    decision_df,

    position_df
):

    rows = []

    # -----------------------------------
    # SELL ACTIONS
    # -----------------------------------

    for _, row in decision_df.iterrows():

        if row["decision"] == "REDUCE":

            rows.append({

                "symbol":
                    row["symbol"],

                "action":
                    "SELL",

                "trade_value":
                    row["trade_value"],

                "priority":
                    row["priority"],

                "reason":
                    row["reason"]
            })

    # -----------------------------------
    # EXCLUDE EXISTING SELL SYMBOLS
    # -----------------------------------

    sell_symbols = set(

        decision_df[
            decision_df[
                "decision"
            ] == "REDUCE"
        ][
            "symbol"
        ]
    )


    # -----------------------------------
    # SETTINGS
    # -----------------------------------

    max_positions = 10

    buy_count = 0

    min_trade_value = 1000

    # -----------------------------------
    # AVAILABLE CASH
    # -----------------------------------

    available_cash = (

        decision_df[
            "trade_value"
        ].sum()
    )

    # -----------------------------------
    # BUY CANDIDATES
    # -----------------------------------

    buy_candidates = (

        position_df.sort_values(

            by="suggested_position_value",

            ascending=False
        )
    )

    for _, row in buy_candidates.iterrows():

        if buy_count >= max_positions:

            break

        symbol = row["symbol"]

        if symbol in sell_symbols:

            continue

        trade_value = round(

            row[
                "suggested_position_value"
            ],

            2
        )

        # Skip tiny allocations

        if trade_value < min_trade_value:

            continue

        # Don't exceed available cash

        if trade_value > available_cash:

            continue

        rows.append({

            "symbol":
                symbol,

            "action":
                "BUY",

            "trade_value":
                trade_value,

            "priority":
                "MEDIUM",

            "reason":
                row[
                    "explanation"
                ]
        })

        available_cash -= trade_value

        buy_count += 1


    print(

        f"\nRemaining cash: £{round(available_cash,2)}"
    )

    # -----------------------------------
    # RETURN RESULTS
    # -----------------------------------

    result_df = pd.DataFrame(

        rows
    )

    return result_df