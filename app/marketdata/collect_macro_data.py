from pathlib import Path
from datetime import datetime
import logging

import pandas as pd
import yfinance as yf

# -----------------------------------
# BASE PATHS
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

csv_path = (
    BASE_DIR
    / "data"
    / "macro_data"
    / "macro_market_ohlcv.csv"
)

log_path = (
    BASE_DIR
    / "logs"
    / "macro_data.log"
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
# MACRO INSTRUMENTS
# -----------------------------------

macro_instruments = [

    "SPY",
    "QQQ",
    "DIA",
    "IWM",
    "^FTSE",
    "^GSPC",
    "^IXIC",
    "^VIX",
    "^VXN",
    "GBPUSD=X",
    "DX-Y.NYB",
    "GC=F",
    "SI=F",
    "CL=F",
    "SMH",
    "SOXX",
    "NVDA",
    "TSM",
    "^TNX"
]

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
        "Created macro_market_ohlcv.csv"
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
            "\nMacro market data already "
            "collected today."
        )

        logging.warning(
            "Collection skipped | "
            f"Data already exists for "
            f"{today_str}"
        )

        raise SystemExit

# -----------------------------------
# COLLECT MACRO DATA
# -----------------------------------

macro_data = []

print(
    "\nCollecting macro OHLCV data...\n"
)

for symbol in macro_instruments:

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

        macro_data.append(row)

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

macro_df = pd.DataFrame(
    macro_data
)

# -----------------------------------
# APPEND TO CSV
# -----------------------------------

macro_df.to_csv(

    csv_path,

    mode="a",

    header=False,

    index=False
)

logging.info(
    f"CSV updated | "
    f"Rows added={len(macro_df)}"
)

print(
    "\nMacro market data collection "
    "complete.\n"
)

logging.info(
    "Macro market data collection complete"
)