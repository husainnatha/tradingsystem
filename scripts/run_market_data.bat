@echo off

cd /d C:\Users\Husain\OneDrive\TradingSystem

call venv\Scripts\activate

python -m app.marketdata.collect_market_data

echo.
echo Market data collection complete.

pause