from collections import defaultdict

from app.database.db import SessionLocal
from app.database.models import Transaction


def get_same_day_matches():

    session = SessionLocal()

    transactions = session.query(
        Transaction
    ).order_by(
        Transaction.trade_date,
        Transaction.transaction_id
    ).all()

    grouped = defaultdict(list)

    # -----------------------------------
    # GROUP TRANSACTIONS
    # -----------------------------------

    for tx in transactions:

        key = (
            tx.symbol,
            tx.trade_date
        )

        grouped[key].append(tx)

    matches = []

    unmatched_sells = []

    remaining_buy_lots = []

    # -----------------------------------
    # PROCESS GROUPS
    # -----------------------------------

    for key, txs in grouped.items():

        buys = []
        sells = []

        # -----------------------------------
        # BUILD WORKING BUY LOTS
        # -----------------------------------

        for tx in txs:

            if tx.action.upper() == "BUY":

                buys.append({

                    "transaction":
                        tx,

                    "remaining_qty":
                        tx.quantity
                })

            elif tx.action.upper() == "SELL":

                sells.append({

                    "transaction":
                        tx,

                    "remaining_qty":
                        tx.quantity
                })

        # -----------------------------------
        # MATCH SELLS AGAINST BUYS
        # -----------------------------------

        for sell_lot in sells:

            sell_tx = sell_lot["transaction"]

            for buy_lot in buys:

                if sell_lot["remaining_qty"] <= 0:

                    break

                available_buy_qty = (
                    buy_lot["remaining_qty"]
                )

                if available_buy_qty <= 0:

                    continue

                matched_qty = min(

                    sell_lot["remaining_qty"],

                    available_buy_qty
                )

                if matched_qty <= 0:

                    continue

                # -----------------------------------
                # RECORD MATCH
                # -----------------------------------

                match = {

                    "symbol":
                        sell_tx.symbol,

                    "trade_date":
                        sell_tx.trade_date,

                    "sell_transaction_id":
                        sell_tx.transaction_id,

                    "buy_transaction_id":
                        buy_lot[
                            "transaction"
                        ].transaction_id,

                    "matched_quantity":
                        matched_qty,

                    "rule":
                        "SAME_DAY"
                }

                matches.append(match)

                # -----------------------------------
                # REDUCE LOT QUANTITIES
                # -----------------------------------

                sell_lot[
                    "remaining_qty"
                ] -= matched_qty

                buy_lot[
                    "remaining_qty"
                ] -= matched_qty

        # -----------------------------------
        # STORE UNMATCHED SELLS
        # -----------------------------------

        for sell_lot in sells:

            if sell_lot[
                "remaining_qty"
            ] > 0:

                unmatched_sells.append({

                    "transaction":
                        sell_lot["transaction"],

                    "remaining_qty":
                        sell_lot["remaining_qty"]
                })

        # -----------------------------------
        # STORE REMAINING BUYS
        # -----------------------------------

        for buy_lot in buys:

            if buy_lot[
                "remaining_qty"
            ] > 0:

                remaining_buy_lots.append({

                    "transaction":
                        buy_lot["transaction"],

                    "remaining_qty":
                        buy_lot["remaining_qty"]
                })

    session.close()

    return {

        "matches":
            matches,

        "unmatched_sells":
            unmatched_sells,

        "remaining_buy_lots":
            remaining_buy_lots
    }

from datetime import timedelta


def get_thirty_day_matches():

    same_day_results = (
        get_same_day_matches()
    )

    unmatched_sells = (
        same_day_results[
            "unmatched_sells"
        ]
    )

    remaining_buy_lots = (
        same_day_results[
            "remaining_buy_lots"
        ]
    )

    matches = []

    # -----------------------------------
    # PROCESS UNMATCHED SELLS
    # -----------------------------------

    for sell_lot in unmatched_sells:

        sell_tx = sell_lot[
            "transaction"
        ]

        sell_date = sell_tx.trade_date

        sell_symbol = sell_tx.symbol

        for buy_lot in remaining_buy_lots:

            buy_tx = buy_lot[
                "transaction"
            ]

            # -----------------------------------
            # SYMBOL MUST MATCH
            # -----------------------------------

            if buy_tx.symbol != sell_symbol:

                continue

            # -----------------------------------
            # BUY MUST BE AFTER SELL
            # -----------------------------------

            if buy_tx.trade_date <= sell_date:

                continue

            # -----------------------------------
            # MUST BE WITHIN 30 DAYS
            # -----------------------------------

            if buy_tx.trade_date > (
                sell_date + timedelta(days=30)
            ):

                continue

            # -----------------------------------
            # CHECK QUANTITIES
            # -----------------------------------

            available_buy_qty = (
                buy_lot["remaining_qty"]
            )

            if available_buy_qty <= 0:

                continue

            if sell_lot[
                "remaining_qty"
            ] <= 0:

                break

            matched_qty = min(

                sell_lot["remaining_qty"],

                available_buy_qty
            )

            if matched_qty <= 0:

                continue

            # -----------------------------------
            # RECORD MATCH
            # -----------------------------------

            match = {

                "symbol":
                    sell_symbol,

                "sell_transaction_id":
                    sell_tx.transaction_id,

                "buy_transaction_id":
                    buy_tx.transaction_id,

                "matched_quantity":
                    matched_qty,

                "rule":
                    "THIRTY_DAY"
            }

            matches.append(match)

            # -----------------------------------
            # REDUCE QUANTITIES
            # -----------------------------------

            sell_lot[
                "remaining_qty"
            ] -= matched_qty

            buy_lot[
                "remaining_qty"
            ] -= matched_qty

    return {

        "same_day_results":
            same_day_results,

        "thirty_day_matches":
            matches,

        "remaining_buy_lots":
            remaining_buy_lots,

        "unmatched_sells":
            unmatched_sells
    }

def get_section_104_pool():

    results = get_thirty_day_matches()

    remaining_buy_lots = (
        results[
            "remaining_buy_lots"
        ]
    )

    unmatched_sells = (
        results[
            "unmatched_sells"
        ]
    )

    pool = {}

    # -----------------------------------
    # BUILD SECTION 104 POOLS
    # -----------------------------------

    for buy_lot in remaining_buy_lots:

        tx = buy_lot["transaction"]

        symbol = tx.symbol

        qty = buy_lot[
            "remaining_qty"
        ]

        if qty <= 0:

            continue

        price_gbp = (

            tx.trade_price *

            tx.fx_rate_to_gbp
        )

        total_cost = (

            qty *

            price_gbp
        )

        if symbol not in pool:

            pool[symbol] = {

                "total_quantity":
                    0,

                "total_cost":
                    0
            }

        pool[symbol][
            "total_quantity"
        ] += qty

        pool[symbol][
            "total_cost"
        ] += total_cost

    # -----------------------------------
    # APPLY UNMATCHED SELLS
    # -----------------------------------

    s104_disposals = []

    for sell_lot in unmatched_sells:

        sell_tx = sell_lot[
            "transaction"
        ]

        remaining_qty = sell_lot[
            "remaining_qty"
        ]

        if remaining_qty <= 0:

            continue

        symbol = sell_tx.symbol

        if symbol not in pool:

            continue

        pool_qty = pool[symbol][
            "total_quantity"
        ]

        pool_cost = pool[symbol][
            "total_cost"
        ]

        if pool_qty <= 0:

            continue

        avg_cost = (
            pool_cost / pool_qty
        )

        matched_cost = (
            remaining_qty *
            avg_cost
        )

        disposal = {

            "symbol":
                symbol,

            "sell_transaction_id":
                sell_tx.transaction_id,

            "matched_quantity":
                remaining_qty,

            "average_cost":
                avg_cost,

            "matched_cost":
                matched_cost,

            "rule":
                "SECTION_104"
        }

        s104_disposals.append(
            disposal
        )

        # -----------------------------------
        # REDUCE POOL
        # -----------------------------------

        pool[symbol][
            "total_quantity"
        ] -= remaining_qty

        pool[symbol][
            "total_cost"
        ] -= matched_cost

    return {

        "same_day_results":
            results[
                "same_day_results"
            ],

        "thirty_day_matches":
            results[
                "thirty_day_matches"
            ],

        "section_104_disposals":
            s104_disposals,

        "remaining_pool":
            pool
    }