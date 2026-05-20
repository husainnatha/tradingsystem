from pathlib import Path
from datetime import datetime
import logging

import pandas as pd
import yfinance as yf

# -----------------------------------
# BASE PATHS
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

excel_path = (
    BASE_DIR
    / "dashboard"
    / "trading_system.xlsx"
)

csv_path = (
    BASE_DIR
    / "data"
    / "market_data"
    / "daily_stock_ohlcv.csv"
)

log_path = (
    BASE_DIR
    / "logs"
    / "market_data.log"
)

# -----------------------------------
# ENSURE DIRECTORIES EXIST
# -----------------------------------

csv_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

log_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

# -----------------------------------
# CONFIGURE LOGGING
# -----------------------------------

logging.basicConfig(

    filename=log_path,

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)


# -----------------------------------
# EXECUTION WINDOW
# -----------------------------------

now = datetime.now()

current_hour = now.hour
current_minute = now.minute

weekday = now.weekday()

is_weekday = weekday <= 4

valid_time = (

    (current_hour == 22 and current_minute >= 15)

    or

    (current_hour == 23)
)

if not is_weekday or not valid_time:

    print(
        "\nExecution blocked.\n"
        "Allowed window:\n"
        "Mon-Fri | 10:15 PM - 11:59 PM"
    )

    logging.warning(
        "Execution blocked | "
        "Outside permitted time window"
    )

    raise SystemExit

# -----------------------------------
# CSV COLUMNS
# -----------------------------------

csv_columns = [

    "collected_timestamp",
    "date",
    "symbol",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "source"
]

# -----------------------------------
# CREATE CSV IF MISSING
# -----------------------------------

if not csv_path.exists():

    empty_df = pd.DataFrame(
        columns=csv_columns
    )

    empty_df.to_csv(
        csv_path,
        index=False
    )

    logging.info(
        "Created daily_stock_ohlcv.csv"
    )

# -----------------------------------
# LOAD WATCHLIST
# -----------------------------------

watchlist_df = pd.read_excel(
    excel_path,
    sheet_name="watchlist"
)

symbols = (

    watchlist_df["symbol"]

    .dropna()

    .astype(str)

    .str.upper()

    .unique()
)

logging.info(
    f"Symbols loaded | Count={len(symbols)}"
)

# -----------------------------------
# PREVENT DUPLICATE NIGHTLY RUNS
# -----------------------------------

existing_df = pd.read_csv(
    csv_path
)

today_str = str(
    datetime.now().date()
)

if not existing_df.empty:

    existing_dates = (

        existing_df["date"]

        .astype(str)

        .unique()
    )

    if today_str in existing_dates:

        print(
            "\nStock market data already "
            "collected today."
        )

        logging.warning(
            "Collection skipped | "
            f"Data already exists for "
            f"{today_str}"
        )

        raise SystemExit

# -----------------------------------
# COLLECT MARKET DATA
# -----------------------------------

logging.info(
    "Stock market data collection started"
)

market_data = []

print(
    "\nCollecting stock OHLCV data...\n"
)

for symbol in symbols:

    try:

        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period="1d"
        )

        if history.empty:

            print(
                f"Skipped: {symbol} | "
                f"No market data"
            )

            continue

        latest = history.iloc[-1]

        row = {

            "collected_timestamp":
                datetime.now(),

            "date":
                datetime.now().date(),

            "symbol":
                symbol,

            "open":
                float(latest["Open"]),

            "high":
                float(latest["High"]),

            "low":
                float(latest["Low"]),

            "close":
                float(latest["Close"]),

            "volume":
                float(latest["Volume"]),

            "source":
                "YahooFinance"
        }

        market_data.append(row)

        print(
            f"Collected: "
            f"{symbol} | "
            f"Close={row['close']}"
        )

        logging.info(
            f"Collected {symbol}"
        )

    except Exception as e:

        print(
            f"Error collecting "
            f"{symbol}: {e}"
        )

        logging.error(
            f"Error collecting "
            f"{symbol}: {e}"
        )

# -----------------------------------
# CREATE DATAFRAME
# -----------------------------------

market_df = pd.DataFrame(
    market_data
)

# -----------------------------------
# APPEND TO CSV
# -----------------------------------

market_df.to_csv(

    csv_path,

    mode="a",

    header=False,

    index=False
)

logging.info(
    f"CSV updated | "
    f"Rows added={len(market_df)}"
)

print(
    "\nStock market data collection "
    "complete.\n"
)

logging.info(
    "Stock market data collection complete"
)